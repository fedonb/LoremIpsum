<template>
  <div class="content">
    <div class="row">
      <div class="col-sm-10">
        <h1>Hotels</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button v-if="isAuthenticated" type="button" class="btn btn-success btn-sm"
                v-b-modal.hotel-modal>Add Hotel</button>
        <br><br>
        <v-card>
          <v-card-title>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
            <v-data-table
              :headers="headers"
              :items="hotels"
              class="elevation-1"
              :loading="loading" loading-text="Loading... Please wait"
              :search="search"
              @click:row="goToBookings(hotels.name)"
            >
            <template slot="items" scope="hotel">
              <tr>
                <td>{{ hotel.name }}</td>
                <td>{{ hotel.address }}</td>
                <td>
                  <div v-if="isAuthenticated" class="btn-group" role="group">
                    <button
                            type="button"
                            class="btn btn-warning btn-sm"
                            v-b-modal.hotel-update-modal
                            @click="editHotel(hotel)">
                        Update
                    </button>
                    <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeleteHotel(hotel)">
                        Delete
                    </button>
                  </div>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Address</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(hotel, index) in hotels" :key="index" @click="goToBookings(hotels.name)">
              <td><a>{{ hotel.name }}</a></td>
              <td>{{ hotel.address }}</td>
              <td>
                <div v-if="isAuthenticated" class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.hotel-update-modal
                          @click="editHotel(hotel)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteHotel(hotel)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addHotelModal"
            id="hotel-modal"
            title="Add a new hotel"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addHotelForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-address-group"
                      label="Address:"
                      label-for="form-address-input">
            <b-form-input id="form-address-input"
                          type="text"
                          v-model="addHotelForm.address"
                          required
                          placeholder="Enter address">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editHotelModal"
            id="hotel-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-name-edit-group"
                    label="Name:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-address-edit-group"
                      label="Address:"
                      label-for="form-address-edit-input">
            <b-form-input id="form-address-edit-input"
                          type="text"
                          v-model="editForm.address"
                          required
                          placeholder="Enter address">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>
<style lang="css" scoped>
.elevation-1 >>> tbody tr :hover {
  cursor: pointer;
}
</style>
<script>
import axios from 'axios'
import Alert from './Alert.vue'

export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  },
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Name',
          align: 'start',
          value: 'name'
        },
        { text: 'Address', value: 'address' },
        { text: ' ', value: 'edit' },
        { text: ' ', value: 'delete' }
      ],
      hotels: [],
      addHotelForm: {
        name: '',
        address: ''
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        address: ''
      }
    }
  },
  components: {
    alert: Alert
  },
  methods: {
    goToBookings (name) {
      this.$router.push({ name: 'Bookings', params: { hotels: name } })
    },
    getHotels () {
      const path = 'http://localhost:5000/hotels'
      axios.get(path)
        .then((res) => {
          this.hotels = res.data.hotels
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    addHotel (payload) {
      const path = 'http://localhost:5000/hotels'
      axios.post(path, payload)
        .then(() => {
          this.getHotels()
          this.message = 'Hotel added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getHotels()
        })
    },
    initForm () {
      this.addHotelForm.name = ''
      this.addHotelForm.address = ''
      this.editForm.id = ''
      this.editForm.name = ''
      this.editForm.address = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addHotelModal.hide()
      // let read = false;
      // if (this.addHotelForm.read[0]) read = true;
      const payload = {
        name: this.addHotelForm.name,
        address: this.addHotelForm.address
      }
      this.addHotel(payload)
      this.initForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addHotelModal.hide()
      this.initForm()
    },
    editHotel (hotel) {
      this.editForm = hotel
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editHotelModal.hide()
      // let read = false;
      // if (this.editForm.read[0]) read = true;
      const payload = {
        name: this.editForm.name,
        address: this.editForm.address
      }
      this.updateHotel(payload, this.editForm.id)
    },
    updateHotel (payload, hotelID) {
      const path = `http://localhost:5000/hotels/${hotelID}`
      axios.put(path, payload)
        .then(() => {
          this.getHotels()
          this.message = 'Hotel updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getHotels()
        })
    },
    onResetUpdate (evt) {
      evt.preventDefault()
      this.$refs.editHotelModal.hide()
      this.initForm()
      this.getHotels() // why?
    },
    removeHotel (hotelID) {
      const path = `http://localhost:5000/hotels/${hotelID}`
      axios.delete(path)
        .then(() => {
          this.getHotels()
          this.message = 'Hotel removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getHotels()
        })
    },
    onDeleteHotel (hotel) {
      this.removeHotel(hotel.id)
    }
  },
  created () {
    this.getHotels()
  }
}
</script>
