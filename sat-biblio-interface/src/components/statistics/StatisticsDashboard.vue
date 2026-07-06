<template>
  <BContainer>
    <AppTitle info="Statistiques agrégées sur le catalogue de la bibliothèque."
              id="id-statistiques">
      Statistiques
    </AppTitle>

    <div v-if="loading" class="text-center my-5">
      <BSpinner label="Chargement..."/>
      <p class="mt-2">Chargement des statistiques...</p>
    </div>

    <BAlert :model-value="error !== ''" variant="danger">
      {{ error }}
    </BAlert>

    <template v-if="!loading && error === ''">
      <!-- Histogrammes des années (obtention puis publication) -->
      <BCard v-for="histo in yearHistograms" :key="histo.id" class="mb-4">
        <BCardHeader class="fw-bold bg-primary-subtle">{{ histo.title }}</BCardHeader>
        <BCardBody>
          <p class="text-muted small mb-3">{{ histo.subtitle }}</p>
          <div v-if="histo.id === 'publication'"
               class="d-flex align-items-center gap-2 mb-3">
            <label for="id-publication-step" class="form-label mb-0 small">
              Pas de l'histogramme :
            </label>
            <BFormSelect id="id-publication-step" v-model="publicationStep"
                         :options="stepOptions" size="sm" class="w-auto"/>
          </div>
          <div v-if="histo.chart.bars.length === 0" class="text-muted fst-italic">
            Aucune donnée disponible.
          </div>
          <div v-else class="chart-scroll">
            <svg :width="histo.chart.width" :height="chartHeight + labelSpace"
                 role="img" :aria-label="histo.title">
              <rect v-for="bar in histo.chart.bars" :key="`b-${bar.year}`"
                    :x="bar.x" :y="bar.y" :width="bar.width" :height="bar.height"
                    rx="2" class="bar">
                <title>{{ bar.label }} : {{ bar.count }}</title>
              </rect>
              <text v-for="bar in histo.chart.bars.filter(b => b.showLabel)" :key="`l-${bar.year}`"
                    :x="bar.x + bar.width / 2" :y="chartHeight + 14"
                    text-anchor="end" class="bar-label"
                    :transform="`rotate(-60 ${bar.x + bar.width / 2} ${chartHeight + 14})`">
                {{ bar.year }}
              </text>
              <line x1="0" :y1="chartHeight" :x2="histo.chart.width" :y2="chartHeight" class="axis"/>
            </svg>
          </div>
        </BCardBody>
      </BCard>

      <!-- Répartition par cote -->
      <BCard class="mb-4">
        <BCardHeader class="fw-bold bg-primary-subtle">Répartition par cote</BCardHeader>
        <BCardBody>
          <p class="text-muted small mb-3">
            Nombre d'enregistrements par préfixe de cote ({{ coteTotal }} au total).
          </p>
          <div v-if="cotes.length === 0" class="text-muted fst-italic">
            Aucune donnée disponible.
          </div>
          <div v-else>
            <div v-for="cote in cotes" :key="cote.prefix"
                 class="d-flex align-items-center mb-2">
              <div class="cote-label text-end me-2 fw-semibold">{{ cote.prefix }}</div>
              <div class="cote-track flex-grow-1">
                <div class="cote-bar" :style="{ width: coteBarWidth(cote.count) }"></div>
              </div>
              <div class="cote-count ms-2 text-end">{{ cote.count }}</div>
            </div>
          </div>
        </BCardBody>
      </BCard>

      <!-- Carte des lieux de publication -->
      <BCard class="mb-4">
        <BCardHeader class="fw-bold bg-primary-subtle">Lieux de publication</BCardHeader>
        <BCardBody>
          <p class="text-muted small mb-3">
            {{ publicationPlaces.length }} lieux localisés ({{ placesLocated }} références).
            <span v-if="placesUnlocated > 0">
              {{ placesUnlocated }} références au lieu inconnu ne sont pas affichées.
            </span>
          </p>
          <div v-if="publicationPlaces.length === 0" class="text-muted fst-italic">
            Aucun lieu localisé.
          </div>
          <div v-else ref="mapEl" class="stat-map"></div>
        </BCardBody>
      </BCard>
    </template>
  </BContainer>
</template>

<script>
import AppTitle from "@/components/visuel/AppTitle.vue";
import { getCatalogueStatistics } from "@/services/api.js";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

// Corrige les chemins des icônes par défaut de Leaflet avec le bundler (Vite).
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default {
  name: "StatisticsDashboard",
  components: { AppTitle },
  data() {
    return {
      loading: true,
      error: "",
      publicationYears: [],
      publicationStep: 10,
      stepOptions: [
        { value: 1, text: "1 an" },
        { value: 5, text: "5 ans" },
        { value: 10, text: "10 ans" },
        { value: 20, text: "20 ans" },
        { value: 50, text: "50 ans" },
      ],
      cotes: [],
      publicationPlaces: [],
      placesLocated: 0,
      placesUnlocated: 0,
      chartHeight: 240,
      labelSpace: 50,
    };
  },
  mounted() {
    this.retrieve();
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  },
  methods: {
    retrieve() {
      this.loading = true;
      this.error = "";
      getCatalogueStatistics().then((response) => {
        if (response.data.success) {
          this.publicationYears = response.data.publication_years || [];
          this.cotes = response.data.cotes || [];
          this.publicationPlaces = response.data.publication_places || [];
          this.placesLocated = response.data.publication_places_located || 0;
          this.placesUnlocated = response.data.publication_places_unlocated || 0;
        } else {
          this.error = "Impossible de récupérer les statistiques.";
        }
      }).catch((reason) => {
        console.error(reason);
        this.error = "Une erreur est survenue lors du chargement des statistiques.";
      }).finally(() => {
        this.loading = false;
        this.$nextTick(() => {
          if (this.error === "" && this.publicationPlaces.length > 0) {
            this.initMap();
          }
        });
      });
    },

    initMap() {
      const el = this.$refs.mapEl;
      if (!el) return;
      if (this.map) {
        this.map.remove();
        this.map = null;
      }
      // Centré sur Tours (siège de la Société Archéologique de Touraine).
      this.map = L.map(el).setView([47.3941, 0.6848], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap",
        maxZoom: 18,
      }).addTo(this.map);

      const bounds = [];
      for (const place of this.publicationPlaces) {
        L.marker([place.lat, place.lon])
          .addTo(this.map)
          .bindPopup(this.buildPlacePopup(place));
        bounds.push([place.lat, place.lon]);
      }
      if (bounds.length > 0) {
        this.map.fitBounds(bounds, { padding: [30, 30] });
      }
    },

    // Construit le contenu de la popup d'un marqueur : nom du lieu, nombre de
    // publications et lien vers le catalogue filtré sur ce lieu de publication.
    buildPlacePopup(place) {
      const container = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = place.place;
      container.appendChild(title);
      container.appendChild(document.createElement("br"));
      container.appendChild(
        document.createTextNode(`${place.count} publication(s)`)
      );
      container.appendChild(document.createElement("br"));

      const target = { name: "catalogue", query: { lieu_publication: place.place } };
      const link = document.createElement("a");
      link.href = this.$router.resolve(target).href;
      link.textContent = "Voir les enregistrements";
      // Navigation SPA au clic gauche ; le href réel permet « ouvrir dans un
      // nouvel onglet » et le clic-milieu.
      link.addEventListener("click", (event) => {
        if (event.defaultPrevented || event.button !== 0
            || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
          return;
        }
        event.preventDefault();
        this.$router.push(target);
      });
      container.appendChild(link);
      return container;
    },

    // Construit la géométrie d'un histogramme vertical à partir de [{year, count}].
    buildVerticalChart(data) {
      const barWidth = 16;
      const gap = 6;
      const height = this.chartHeight;
      const maxCount = Math.max(1, ...data.map((d) => d.count));
      const labelStep = Math.max(1, Math.ceil(data.length / 30));
      const bars = data.map((d, i) => {
        const h = (d.count / maxCount) * height;
        return {
          year: d.year,
          label: d.label ?? d.year,
          count: d.count,
          x: i * (barWidth + gap),
          y: height - h,
          width: barWidth,
          height: h,
          showLabel: i % labelStep === 0,
        };
      });
      const width = Math.max(data.length * (barWidth + gap), 1);
      return { bars, width, maxCount };
    },

    // Regroupe [{year, count}] par tranches de `step` années.
    // Le libellé d'une tranche est l'intervalle couvert (ex. « 1900–1909 »).
    binYears(data, step) {
      const size = Number(step);
      if (size <= 1) return data;
      const bins = new Map();
      for (const d of data) {
        const start = Math.floor(d.year / size) * size;
        bins.set(start, (bins.get(start) || 0) + d.count);
      }
      return [...bins.entries()]
        .sort((a, b) => a[0] - b[0])
        .map(([start, count]) => ({
          year: start,
          label: `${start}–${start + size - 1}`,
          count,
        }));
    },

    yearRange(data) {
      if (data.length === 0) return "";
      return `${data[0].year}–${data[data.length - 1].year}`;
    },

    totalCount(data) {
      return data.reduce((sum, d) => sum + d.count, 0);
    },

    coteBarWidth(count) {
      const max = Math.max(1, ...this.cotes.map((c) => c.count));
      return `${(count / max) * 100}%`;
    },
  },
  computed: {
    yearHistograms() {
      return [
        {
          id: "publication",
          title: "Années de publication",
          subtitle: this.publicationYears.length === 0
            ? ""
            : `${this.totalCount(this.publicationYears)} références avec une année définie (${this.yearRange(this.publicationYears)}).`,
          chart: this.buildVerticalChart(this.binYears(this.publicationYears, this.publicationStep)),
        },
      ];
    },
    coteTotal() {
      return this.totalCount(this.cotes);
    },
  },
};
</script>

<style scoped>
.chart-scroll {
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.bar {
  fill: var(--bs-primary, #0d6efd);
  transition: fill 0.15s ease;
}

.bar:hover {
  fill: var(--bs-primary-text-emphasis, #0a58ca);
}

.bar-label {
  font-size: 10px;
  fill: #495057;
}

.axis {
  stroke: #adb5bd;
  stroke-width: 1;
}

.cote-label {
  width: 4.5rem;
  flex: 0 0 4.5rem;
}

.cote-count {
  width: 3.5rem;
  flex: 0 0 3.5rem;
}

.cote-track {
  background-color: var(--bs-primary-bg-subtle, #e2e9f7);
  border-radius: 0.25rem;
  overflow: hidden;
}

.cote-bar {
  height: 1.25rem;
  background-color: var(--bs-primary, #0d6efd);
  border-radius: 0.25rem;
}

.stat-map {
  height: 480px;
  width: 100%;
  border-radius: 0.25rem;
  z-index: 0;
}
</style>
