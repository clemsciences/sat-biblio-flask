<template>
<!--  -->
  <BContainer>
    <h2>Imports</h2>

    <BRow>
      <UploadCatalogueView @upload-finished="refreshImportList"/>
<!--      <BButton @click="uploadCatalogue">Téléverser un catalogue</BButton>-->
    </BRow>
    <BRow>

    <BCol cols="6">
      <BCard>:
        <BCardBody>
          <div v-if="catalogueNumber > 0">
            <p>Cliquez sur la ligne pour voir les détails.</p>
<!--              <BListGroup v-for="item in importList" :key="`id-${item.id}`">-->
<!--                <BListGroupItem>{{ item }}</BListGroupItem>-->
<!--              </BListGroup>-->
            <BTable ref="importsTable" responsive striped bordered hover :items="loadImports"
                     :fields="fields" primary-key="key"
                     :per-page="perPage" :current-page="currentPage"
                     :sort-by="sortBy" selectable select-mode="single"
                     @row-clicked="showCatalogueView" :filter="onFilter">
<!--                @row-dblclicked="goToImport"-->
              <template #cell(datetime)="data">
                <i>{{ new Date(data.item.datetime).toLocaleDateString() }}</i>
              </template>
              <template #cell(actions)="row">

                <BButton :disabled="row.item.key !== selectedKey"
                          size="sm" class="me-1"
                          v-b-toggle.suppression :id="`delete-${row.item.key}`">
                  Supprimer
                </BButton>
                <BTooltip :target="`delete-${row.item.key}`" triggers="hover"
                           style="text-justify: auto;">
                  Supprimer le fichier <b>{{ row.item.filename }}</b>.
                  &Ccedil;a ne supprime pas l'import associé.
                </BTooltip>
              </template>

            </BTable>
            <BPagination
              v-model="currentPage"
              :total-rows="catalogueNumber"
              :per-page="perPage"
              aria-controls="my-table"
              class="my-3"/>
          </div>

          <div v-else>
            <h5>Aucun import n'a été fait.</h5>
          </div>
        </BCardBody>
      </BCard>
<!--    </BRow>-->
<!--    <BRow>-->
    </BCol>
    <BCol cols="6">
        <BCard>
          <BCardBody>
            <div v-if="selectedImportId === null">
              <p>Sélectionnez un catalogue</p>
            </div>
            <div v-else-if="selectedImportId === -1">
              <ImportItemCreation :selected-key="selectedKey"/>
            </div>
            <div v-else>
              <ImportItemView :import-item-id="selectedImportId"/>
            </div>
          </BCardBody>
        </BCard>
    </BCol>
    </BRow>
    <BModal id="suppression" title="Suppression de l'import"
      cancel-title="Annuler" ok-title="Supprimer" @ok="deleteFile">
      <p>Êtes-vous sûr de supprimer le fichier <b>{{ selectedFilename }}</b>?</p>
    </BModal>

  </BContainer>
</template>

<script>
import {
  getCataloguesCountRequest,
  getCatalogueListRequest,
  getCatalogueImportByKey,
  deleteCatalogueByKey
} from "@/services/api";
import ImportItemCreation from "@/components/import/ImportItemCreation.vue";
import UploadCatalogueView from "@/components/import/UploadCatalogueView.vue";
import ImportItemView from "@/components/import/ImportItemView.vue";
import {BCard, BCardBody, BCol, BContainer, BRow} from "bootstrap-vue-next";

export default {
  name: "ImportList",
  components: {BCardBody, BCard, BRow, BContainer, BCol, UploadCatalogueView, ImportItemCreation, ImportItemView},
  data: function() {
    return {
      // region list
      cataloguesList: [],
      currentPage: 1,
      perPage: 5,
      sortBy: "date",
      descriptionFilter: "",
      catalogueNumber: 0,
      selectedImportId: null,
      selectedKey: "",
      fields: [
        {
          key: 'filename',
          label: "Nom de fichier",
          sortable: true,
        },
        {
          key: 'datetime',
          label: "Date",
          sortable: true,
        },
        {
          key: 'key',
          label: 'Clé',
          sortable: false,
        },
        {
          key: 'actions',
          label: 'Actions',
          sortable: false
        }
      ],
      // endregion

      file: null,
      isProcessing: false,
    };
  },
  mounted() {
    this.getImportTotalNumber();
  },
  methods: {
    loadImports: function(ctx, callback) {
      console.log("loadImports");
      const params = `?page=${ctx.currentPage}&size=${ctx.perPage}&sortBy=${ctx.sortBy}`;
      let filterParams = "";
      if (this.descriptionFilter.length > 0) {
        filterParams = `${filterParams}&description=${encodeURI(this.descriptionFilter)}`;
      }
      getCatalogueListRequest(params+filterParams).then((response) => {
        if (response.data.success) {
          this.cataloguesList = response.data.catalogues.map(
              (item) => {
                item.datetime = new Date(item.datetime);
                return item;
              });
        } else {
          this.cataloguesList = [];
        }
        callback(this.cataloguesList);
      }).catch(
          (reason) => {
            console.error(reason);
            callback([]);
          }
      );
      return null;
    },
    getImportTotalNumber() {
      let filterParams = "";
      if(this.descriptionFilter.length > 0) {
        filterParams = `${filterParams}?description=${encodeURI(this.descriptionFilter)}`;
      }
      getCataloguesCountRequest(filterParams).then(
          (response) => {
            console.log(response.data);
            this.catalogueNumber = response.data.total_count;
            this.selectedKey = "";
            this.selectedImportId = -1;
            // this.filteredCatalogueNumber = response.data.filtered_count;
          }
      )
    },
    goToImport(item) {
      this.$router.push(`/administrateur/imports/${item.id}`)
    },
    deleteFile() {
      deleteCatalogueByKey(this.selectedKey, this.$store.state.connectionInfo.token).then(
          (response) => {
            if (response.data.success) {
              this.refreshImportList();
            } else {
              console.log(response.data);
            }
          }
      );
    },
    refreshImportList() {
      this.getImportTotalNumber();
      this.$refs.importsTable.refresh();
    },
    showCatalogueView(item) {
      console.log(item);
      this.selectedKey = item.key;
      if (item) {
        getCatalogueImportByKey(item.key).then(
            (response) => {
              if (response.data.success) {
                const importData = response.data.import_data;
                if (importData) {
                    this.selectedImportId = importData.id;
                } else {
                  this.selectedImportId = -1;
                }
              }
            }
        );
      }
    }
  },
  watch: {
    catalogueNumber: function(newValue) {
      console.log(newValue);
    },
    descriptionFilter: function() {
      this.getImportTotalNumber();
      this.currentPage = 1;
    }
  },
  computed: {
    onFilter() {
      return this.descriptionFilter;
    },
    selectedFilename() {
      let item = this.cataloguesList.find((item) => {
        return item.key === this.selectedKey;
      });
      if(item) {
        return item.filename;
      }
      return ''
    }
  }
}
</script>

<style scoped>

</style>