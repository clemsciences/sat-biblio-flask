// Comportement responsive partagé par les vues « liste » (catalogue, références,
// enregistrements, auteurs). Fournit :
//   - `isMobile`    : vrai en dessous du breakpoint `lg` de Bootstrap 5
//   - `filtersOpen` : état d'ouverture du panneau de filtres repliable sur mobile
//
// Le breakpoint (max-width: 991.98px) est aligné sur les colonnes de filtre `lg="4"`.
//
// Vue fusionne les hooks du mixin avec ceux du composant (mixin d'abord), donc une vue
// peut garder son propre `mounted` / `data` sans conflit.

const MOBILE_QUERY = '(max-width: 991.98px)';

export default {
  data() {
    return {
      isMobile: false,
      filtersOpen: false,
    };
  },
  methods: {
    updateIsMobile(mql) {
      this.isMobile = mql.matches;
    },
  },
  mounted() {
    this._mql = window.matchMedia(MOBILE_QUERY);
    this.updateIsMobile(this._mql);
    this._mqlHandler = (e) => this.updateIsMobile(e);
    this._mql.addEventListener('change', this._mqlHandler);
  },
  beforeUnmount() {
    if (this._mql && this._mqlHandler) {
      this._mql.removeEventListener('change', this._mqlHandler);
    }
  },
};
