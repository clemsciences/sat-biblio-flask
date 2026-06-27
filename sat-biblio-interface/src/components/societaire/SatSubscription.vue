<template>
  <BContainer>
    <BRow>
      <BCol cols="12">
        <h3>Adhésion à la SAT</h3>
        <p>Veuillez remplir le formulaire ci-dessous pour adhérer à la société.</p>
      </BCol>
    </BRow>

    <BFormGroup @submit.prevent="onSubmit">
      <fieldset class="mb-4 p-3 border rounded">
        <legend class="w-auto px-2 h5">Première personne</legend>
        <BRow>
          <BCol md="6">
            <BFormGroup label="Prénom" label-for="first-name" label-cols-sm="4">
              <BFormInput id="first-name" v-model.trim="form.firstName" required />
            </BFormGroup>
          </BCol>
          <BCol md="6">
            <BFormGroup label="Nom" label-for="last-name" label-cols-sm="4">
              <BFormInput id="last-name" v-model.trim="form.lastName" required />
            </BFormGroup>
          </BCol>
        </BRow>

        <!-- Informations complémentaires personne 1 -->
        <BRow>
          <BCol md="6">
            <BFormGroup label="Profession ou ancienne profession">
              <BFormInput v-model.trim="form.profession" />
            </BFormGroup>
          </BCol>
          <BCol md="6">
            <BFormGroup label="Année de naissance">
              <BFormInput v-model.trim="form.birthYear" type="number" min="1900" max="2100" />
            </BFormGroup>
          </BCol>
        </BRow>
      </fieldset>

      <BRow>
        <BCol cols="12">
          <BFormGroup label="Adresse complète" label-for="full-address">
            <BFormTextarea id="full-address" v-model.trim="form.address" rows="3" required />
          </BFormGroup>
        </BCol>
      </BRow>

      <BRow>
        <BCol md="4">
          <BFormGroup label="Téléphone fixe" label-for="phone-landline">
            <BFormInput id="phone-landline" v-model.trim="form.phoneLandline" />
          </BFormGroup>
        </BCol>
        <BCol md="4">
          <BFormGroup label="Téléphone mobile" label-for="phone-mobile">
            <BFormInput id="phone-mobile" v-model.trim="form.phoneMobile" />
          </BFormGroup>
        </BCol>
        <BCol md="4">
          <BFormGroup label="Courriel" label-for="email" :state="emailState">
            <BFormInput id="email" type="email" v-model.trim="form.email" />
            <BFormInvalidFeedback v-if="emailState === false">Courriel invalide</BFormInvalidFeedback>
          </BFormGroup>
        </BCol>
      </BRow>

      <BRow>
        <BCol md="6">
          <BFormGroup label="Type d'adhésion">
            <BFormRadioGroup v-model="form.membershipType" name="membership-type">
              <BFormRadio :value="'student'">Étudiant (10 €)</BFormRadio>
              <BFormRadio :value="'single'">Inscription pour une personne (46 €)</BFormRadio>
              <BFormRadio :value="'couple'">Inscription pour un couple (62 €)</BFormRadio>
            </BFormRadioGroup>
            <small class="text-muted d-block mt-1">Montants valables du 1er janvier 2025 au 31 décembre 2025.</small>
          </BFormGroup>
        </BCol>
        <BCol md="6">
          <BFormGroup label="Options">
            <BFormCheckbox v-model="form.receiveBulletinByPost">Recevoir le prochain bulletin par la poste (+13 €)</BFormCheckbox>
            <BFormCheckbox v-model="form.mustReceiveInfoByMail">Je souhaite absolument recevoir les informations par courrier</BFormCheckbox>
            <BFormCheckbox v-model="form.refusePublishInfo">Je refuse que mon nom et mon adresse figurent dans la liste des sociétaires dans le prochain bulletin</BFormCheckbox>
          </BFormGroup>
        </BCol>
      </BRow>

      <fieldset v-if="form.membershipType === 'couple'" class="mb-4 p-3 border rounded">
        <legend class="w-auto px-2 h5">Deuxième personne</legend>
        <BRow>
          <BCol md="6">
            <BFormGroup label="Prénom (2)">
              <BFormInput v-model.trim="form.secondFirstName" />
            </BFormGroup>
          </BCol>
          <BCol md="6">
            <BFormGroup label="Nom (2)">
              <BFormInput v-model.trim="form.secondLastName" />
            </BFormGroup>
          </BCol>
          <BCol md="6">
            <BFormGroup label="Profession ou ancienne profession (2)">
              <BFormInput v-model.trim="form.secondProfession" />
            </BFormGroup>
          </BCol>
          <BCol md="6">
            <BFormGroup label="Année de naissance (2)">
              <BFormInput v-model.trim="form.secondBirthYear" type="number" min="1900" max="2100" />
            </BFormGroup>
          </BCol>
        </BRow>
      </fieldset>

      <BRow>
        <BCol md="6">
          <BFormGroup label="Mode de règlement">
            <BFormRadioGroup v-model="form.paymentMethod" name="payment-method">
              <BFormRadio value="cheque">Chèque</BFormRadio>
              <BFormRadio value="virement">Virement bancaire</BFormRadio>
              <BFormRadio value="carte">Carte bancaire ou espèces à la BHT ou pendant une séance mensuelle</BFormRadio>
            </BFormRadioGroup>
            <BAlert v-if="paymentInstructions" show variant="info" class="mt-2">{{ paymentInstructions }}</BAlert>
          </BFormGroup>
        </BCol>
        <BCol md="6" class="d-flex align-items-center" v-if="form.membershipType">
          <div>
            <div class="h5 mb-1">Montant total</div>
            <div class="display-4">{{ totalAmount }} €</div>
          </div>
        </BCol>
      </BRow>

      <BRow class="mt-3">
        <BCol>
          <BButton type="submit" variant="primary" :disabled="!isValid">Envoyer</BButton>
          <span class="mx-3 text-success">{{ message }}</span>
        </BCol>
      </BRow>
    </BFormGroup>
  </BContainer>
</template>

<script>
import { sendSatSubscription } from "@/services/api";
import {BButton, BCol, BFormGroup, BFormRadio, BRow} from "bootstrap-vue-next";
export default {
  name: "SatSubscription",
  components: {BRow, BFormGroup, BFormRadio, BButton, BCol},
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