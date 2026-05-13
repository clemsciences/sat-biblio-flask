<template>
  <BContainer>
    <h2>Imports</h2>

    <BRow>
      <UploadCatalogueView @upload-finished="refreshImportList"/>
    </BRow>
    <BRow>
      <BCol cols="6">
        <BCard>
          <BCardBody>
            <div v-if="catalogueNumber > 0">
              <p>Cliquez sur la ligne pour voir les détails.</p>
              <BTable ref="importsTable" responsive striped bordered hover
                      :provider="loadImports"
                      :fields="fields"
                      primary-key="key"
                      :per-page="perPage"
                      :current-page="currentPage"
                      :sort-by="tableSortBy"
                      selectable
                      select-mode="single"
                      @row-clicked="showCatalogueView">
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
  getCatalogueListRequest,
  getCatalogueImportByKey,
  deleteCatalogueByKey
} from "@/services/api";
import ImportItemCreation from "@/components/import/ImportItemCreation.vue";
import UploadCatalogueView from "@/components/import/UploadCatalogueView.vue";
import ImportItemView from "@/components/import/ImportItemView.vue";
import {
  BButton,
  BCard,
  BCardBody,
  BCol,
  BContainer,
  BModal,
  BPagination,
  BRow,
  BTable,
  BTooltip
} from "bootstrap-vue-next";

export default {
  name: "ImportList",
  components: {
    BButton, BCard, BCardBody, BCol, BContainer, BModal,
    BPagination, BRow, BTable, BTooltip,
    UploadCatalogueView, ImportItemCreation, ImportItemView
  },
  data() {
    return {
      isMounted: false,
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
        { key: 'filename', label: "Nom de fichier", sortable: true },
        { key: 'datetime', label: "Date",            sortable: true },
        { key: 'key',      label: 'Clé',             sortable: false },
        { key: 'actions',  label: 'Actions',         sortable: false },
      ],
      // endregion
      file: null,
      isProcessing: false,
    };
  },

  computed: {
    // bootstrap-vue-next attend un tableau [{ key, order }] pour le prop sort-by
    tableSortBy() {
      return [{ key: this.sortBy, order: 'asc' }];
    },
    selectedFilename() {
      const item = this.cataloguesList.find((item) => item.key === this.selectedKey);
      return item ? item.filename : '';
    },
  },

  methods: {
    // -----------------------------------------------------------------------
    // Provider — ctx.sortBy est un tableau [{ key, order }] en bvn
    // currentPage et perPage ne sont pas dans ctx : on utilise this.*
    // -----------------------------------------------------------------------
    async loadImports(ctx) {
      const sortKey = Array.isArray(ctx.sortBy) && ctx.sortBy.length > 0
          ? ctx.sortBy[0].key
          : this.sortBy;

      let params = `?page=${this.currentPage}`
          + `&size=${this.perPage}`
          + `&sortBy=${sortKey}`;

      if (this.descriptionFilter.length > 0) {
        params += `&description=${encodeURI(this.descriptionFilter)}`;
      }

      try {
        // ✅ await déjà présent dans l'original, conservé
        const response = await getCatalogueListRequest(params);
        if (response.data.success) {
          this.cataloguesList = (response.data.catalogues ?? []).map((item) => {
            item.datetime = new Date(item.datetime);
            return item;
          });
          // ✅ Total mis à jour avant le return pour que BPagination se recalcule
          this.catalogueNumber = response.data.total_count ?? this.cataloguesList.length;
          return this.cataloguesList;
        }
        this.cataloguesList  = [];
        this.catalogueNumber = 0;
        return [];
      } catch (reason) {
        console.error(reason);
        this.catalogueNumber = 0;
        return [];
      }
    },

    goToImport(item) {
      this.$router.push(`/administrateur/imports/${item.id}`);
    },

    deleteFile() {
      deleteCatalogueByKey(this.selectedKey, this.$store.state.connectionInfo.token).then(
          (response) => {
            if (response.data.success) {
              this.refreshImportList();
            } else {
              console.error(response.data);
            }
          }
      );
    },

    refreshImportList() {
      this.selectedKey      = "";
      this.selectedImportId = -1;
      this.refreshTable();
    },

    refreshTable() {
      this.$refs.importsTable?.refresh();
    },

    showCatalogueView(item) {
      this.selectedKey = item.key;
      getCatalogueImportByKey(item.key).then((response) => {
        if (response.data.success) {
          const importData = response.data.import_data;
          this.selectedImportId = importData ? importData.id : -1;
        }
      });
    },
  },

  mounted() {
    this.$nextTick(() => {
      this.isMounted = true;
    });
  },

  watch: {
    descriptionFilter() {
      if (this.isMounted) this.currentPage = 1;
      this.refreshTable();
    },
    currentPage() {
      this.refreshTable();
    },
  },
}
</script>

<style scoped>
</style>