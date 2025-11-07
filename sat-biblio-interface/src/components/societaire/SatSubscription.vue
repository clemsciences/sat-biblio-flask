<template>
  <b-container>
    <b-row>
      <b-col cols="12">
        <h3>Adhésion à la SAT</h3>
        <p>Veuillez remplir le formulaire ci-dessous pour adhérer à la société.</p>
      </b-col>
    </b-row>

    <b-form @submit.prevent="onSubmit">
      <fieldset class="mb-4 p-3 border rounded">
        <legend class="w-auto px-2 h5">Première personne</legend>
        <b-row>
          <b-col md="6">
            <b-form-group label="Prénom" label-for="first-name" label-cols-sm="4">
              <b-form-input id="first-name" v-model.trim="form.firstName" required />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Nom" label-for="last-name" label-cols-sm="4">
              <b-form-input id="last-name" v-model.trim="form.lastName" required />
            </b-form-group>
          </b-col>
        </b-row>

        <!-- Informations complémentaires personne 1 -->
        <b-row>
          <b-col md="6">
            <b-form-group label="Profession ou ancienne profession">
              <b-form-input v-model.trim="form.profession" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Année de naissance">
              <b-form-input v-model.trim="form.birthYear" type="number" min="1900" max="2100" />
            </b-form-group>
          </b-col>
        </b-row>
      </fieldset>

      <b-row>
        <b-col cols="12">
          <b-form-group label="Adresse complète" label-for="full-address">
            <b-form-textarea id="full-address" v-model.trim="form.address" rows="3" required />
          </b-form-group>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="4">
          <b-form-group label="Téléphone fixe" label-for="phone-landline">
            <b-form-input id="phone-landline" v-model.trim="form.phoneLandline" />
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group label="Téléphone mobile" label-for="phone-mobile">
            <b-form-input id="phone-mobile" v-model.trim="form.phoneMobile" />
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group label="Courriel" label-for="email" :state="emailState">
            <b-form-input id="email" type="email" v-model.trim="form.email" />
            <b-form-invalid-feedback v-if="emailState === false">Courriel invalide</b-form-invalid-feedback>
          </b-form-group>
        </b-col>
      </b-row>

      <b-row>
        <b-col md="6">
          <b-form-group label="Type d'adhésion">
            <b-form-radio-group v-model="form.membershipType" name="membership-type">
              <b-form-radio :value="'student'">Étudiant (10 €)</b-form-radio>
              <b-form-radio :value="'single'">Inscription pour une personne (46 €)</b-form-radio>
              <b-form-radio :value="'couple'">Inscription pour un couple (62 €)</b-form-radio>
            </b-form-radio-group>
            <small class="text-muted d-block mt-1">Montants valables du 1er janvier 2025 au 31 décembre 2025.</small>
          </b-form-group>
        </b-col>
        <b-col md="6">
          <b-form-group label="Options">
            <b-form-checkbox v-model="form.receiveBulletinByPost">Recevoir le prochain bulletin par la poste (+13 €)</b-form-checkbox>
            <b-form-checkbox v-model="form.mustReceiveInfoByMail">Je souhaite absolument recevoir les informations par courrier</b-form-checkbox>
            <b-form-checkbox v-model="form.refusePublishInfo">Je refuse que mon nom et mon adresse figurent dans la liste des sociétaires dans le prochain bulletin</b-form-checkbox>
          </b-form-group>
        </b-col>
      </b-row>

      <fieldset v-if="form.membershipType === 'couple'" class="mb-4 p-3 border rounded">
        <legend class="w-auto px-2 h5">Deuxième personne</legend>
        <b-row>
          <b-col md="6">
            <b-form-group label="Prénom (2)">
              <b-form-input v-model.trim="form.secondFirstName" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Nom (2)">
              <b-form-input v-model.trim="form.secondLastName" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Profession ou ancienne profession (2)">
              <b-form-input v-model.trim="form.secondProfession" />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Année de naissance (2)">
              <b-form-input v-model.trim="form.secondBirthYear" type="number" min="1900" max="2100" />
            </b-form-group>
          </b-col>
        </b-row>
      </fieldset>

      <b-row>
        <b-col md="6">
          <b-form-group label="Mode de règlement">
            <b-form-radio-group v-model="form.paymentMethod" name="payment-method">
              <b-form-radio value="cheque">Chèque</b-form-radio>
              <b-form-radio value="virement">Virement bancaire</b-form-radio>
              <b-form-radio value="carte">Carte bancaire ou espèces à la BHT ou pendant une séance mensuelle</b-form-radio>
            </b-form-radio-group>
            <b-alert v-if="paymentInstructions" show variant="info" class="mt-2">{{ paymentInstructions }}</b-alert>
          </b-form-group>
        </b-col>
        <b-col md="6" class="d-flex align-items-center" v-if="form.membershipType">
          <div>
            <div class="h5 mb-1">Montant total</div>
            <div class="display-4">{{ totalAmount }} €</div>
          </div>
        </b-col>
      </b-row>

      <b-row class="mt-3">
        <b-col>
          <b-button type="submit" variant="primary" :disabled="!isValid">Envoyer</b-button>
          <span class="mx-3 text-success">{{ message }}</span>
        </b-col>
      </b-row>
    </b-form>
  </b-container>
</template>

<script>
import { sendSatSubscription } from "@/services/api";
export default {
  name: "SatSubscription",
  data() {
    return {
      form: {
        firstName: "",
        lastName: "",
        address: "",
        phoneLandline: "",
        phoneMobile: "",
        email: "",
        membershipType: null, // student|single|couple
        receiveBulletinByPost: false,
        paymentMethod: null, // cheque|virement|carte
        mustReceiveInfoByMail: false,
        refusePublishInfo: false,
        profession: "",
        birthYear: 1960,
        secondFirstName: "",
        secondLastName: "",
        secondProfession: "",
        secondBirthYear: 1960
      },
      message: ""
    };
  },
  computed: {
    totalAmount() {
      let base = 0;
      if (this.form.membershipType === "student") base = 10;
      else if (this.form.membershipType === "single") base = 46;
      else if (this.form.membershipType === "couple") base = 62;
      const bulletin = this.form.receiveBulletinByPost ? 13 : 0;
      return base + bulletin;
    },
    emailState() {
      if (!this.form.email) return null;
      // basic email regex
      const re = /[^\s@]+@[^\s@]+\.[^\s@]+/;
      return re.test(this.form.email);
    },
    isValid() {
      return (
        this.form.firstName.trim().length > 0 &&
        this.form.lastName.trim().length > 0 &&
        this.form.address.trim().length > 0 &&
        !!this.form.membershipType &&
        !!this.form.paymentMethod &&
        (this.emailState === null || this.emailState === true)
      );
    },
    paymentInstructions() {
      switch (this.form.paymentMethod) {
        case 'cheque':
          return "Merci d'établir un chèque à l'ordre de la Société archéologique de Touraine. Adresse d'envoi: 37 avenue André Malraux. Vous pouvez aussi déposer le chèque à la BHT.";
        case 'virement':
          return "Effectuez un virement au compte de la SAT (IBAN communiqué). Indiquez en référence: Adhésion SAT - " + this.form.lastName + " " + this.form.firstName + ".";
        case 'carte':
          return "Paiement par carte bancaire ou en espèces à la BHT (mardi 18h-21h ; mercredi et samedi 10h-13h) ou lors des séances mensuelles.";
        default:
          return "";
      }
    }
  },
  methods: {
    async onSubmit() {
      if (!this.isValid) return;
      const payload = {
        ...this.form,
        totalAmount: this.totalAmount
      };
      try {
        const { data } = await sendSatSubscription(payload);
        if (data && data.success) {
          this.message = data.message || "Demande envoyée avec succès.";
        } else {
          this.message = (data && data.message) || "Echec de l'envoi de la demande.";
        }
      } catch (e) {
        this.message = "Echec de l'envoi de la demande.";
        // console.error(e);
      }
    }
  }
};
</script>

<style scoped>
</style>