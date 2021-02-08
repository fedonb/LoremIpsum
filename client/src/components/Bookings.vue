<template>
  <div class="content">
    <div class="row">
      <div class="col-sm-10">
        <h1>Bookings</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm"
                v-b-modal.booking-modal>Add Booking</button>
        <br><br>
        <div class="filter btn-group" role="group">
          <b-dropdown id="form-hotel-input"
                      :text="filteredHotel"
                      v-model="filteredHotel"
                      required
                      width=100%>
            <!-- <b-dropdown-item disabled value=" ">Select a Hotel</b-dropdown-item> -->
            <b-dropdown-item v-for="hotel in hotels"
                        :key="hotel.id"
                        :value="hotel.id"
                        @click="filteredHotel = hotel.name; filteredHotelID = hotel.id">
              {{hotel.name}}
            </b-dropdown-item>
          </b-dropdown>
          <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  @click="clearFilter()">
              Clear Filter
          </button>
        </div>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">From</th>
              <th scope="col">To</th>
              <th scope="col">Name</th>
              <th scope="col">Hotel</th>
              <th scope="col">Confirmed?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(booking, index) in filteredBookings" :key="index">
            <!-- <tr v-for="(booking, index) in bookings" :key="index"> -->
              <td>{{ booking.from }}</td>
              <td>{{ booking.to }}</td>
              <td>{{ booking.name }}</td>
              <td>{{ booking.hotel }}</td>
              <td>
                <span v-if="booking.confirmed">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div v-if="isAuthenticated" class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.booking-update-modal
                          @click.stop="editBooking(booking)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click.stop="onDeleteBooking(booking)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookingModal"
            id="booking-modal"
            title="Add a new booking"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <div id="date" >
        <b-form-group id="form-from-group"
                      label="From:"
                      label-for="form-from-input">
          <datepicker id="form-from-input"
                      v-model="addBookingForm.from"
                      required
                      placeholder="Choose a starting date">
          </datepicker>
        </b-form-group>
      </div>
      <div id="date">
        <b-form-group id="form-to-group"
                      label="To:"
                      label-for="form-to-input">
          <datepicker id="form-to-input"
                      v-model="addBookingForm.to"
                      required
                      placeholder="Choose an ending date">
          </datepicker>
        </b-form-group>
      </div>
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addBookingForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
      <div class="dropdown">
        <b-form-group id="form-hotel-group"
                    label="Hotel:"
                    label-for="form-hotel-input">
          <b-dropdown id="form-hotel-input"
                      :text="selectedHotel"
                      v-model="selectedHotel"
                      required
                      width=100%>
            <!-- <b-dropdown-item disabled value=" ">Select a Hotel</b-dropdown-item> -->
            <b-dropdown-item v-for="hotel in hotels"
                        :key="hotel.id"
                        :value="hotel.id"
                        @click="selectedHotel = hotel.name; selectedHotelID = hotel.id">
              {{hotel.name}}
            </b-dropdown-item>
          </b-dropdown>
        </b-form-group>
      </div>
        <b-form-group v-if="isAuthenticated" id="form-confirmed-group">
          <b-form-checkbox-group v-model="addBookingForm.confirmed" id="form-checks">
            <b-form-checkbox value="true">Confirmed?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editBookingModal"
            id="booking-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <div id="date" >
        <b-form-group id="form-from-group"
                      label="From:"
                      label-for="form-from-input">
          <datepicker id="form-from-input"
                      v-model="editForm.from"
                      @input="formatPicker()"
                      required
                      placeholder="Choose a starting date">
          </datepicker>
        </b-form-group>
      </div>
      <div id="date">
        <b-form-group id="form-to-group"
                      label="To:"
                      label-for="form-to-input">
          <datepicker id="form-to-input"
                      v-model="editForm.to"
                      required
                      placeholder="Choose an ending date">
          </datepicker>
        </b-form-group>
      </div>
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
        <div class="dropdown">
        <b-form-group id="form-hotel-group"
                    label="Hotel:"
                    label-for="form-hotel-input">
          <b-dropdown id="form-hotel-input"
                      :text="selectedHotel"
                      v-model="selectedHotel"
                      required
                      width=100%>
            <!-- <b-dropdown-item disabled value=" ">Select a Hotel</b-dropdown-item> -->
            <b-dropdown-item v-for="hotel in hotels"
                        :key="hotel.id"
                        :value="hotel.id"
                        @click="selectedHotel = hotel.name; selectedHotelID = hotel.id">
              {{hotel.name}}
            </b-dropdown-item>
          </b-dropdown>
        </b-form-group>
      </div>
        <b-form-group id="form-confirmed-edit-group">
          <b-form-checkbox-group v-model="editForm.confirmed" id="form-checks">
            <b-form-checkbox value="true">Confirmed?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>
<style scoped>
.datepicker{z-index:9999 !important}
#date {
    display: inline-block;
    width: 50%;
}

#date label {
    display: block;
}
</style>
<script>
import Datepicker from 'vuejs-datepicker'
import axios from 'axios'
import moment from 'moment'
import Alert from './Alert.vue'

export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    filteredBookings: function () {
      const vm = this
      const hotel = vm.filteredHotel
      if (this.filteredFromParent) {
        const newfilteredHotel = this.filteredHotel
        return vm.bookings.filter(function (bookings) {
          return bookings.hotel === newfilteredHotel
        })
      } else if (hotel === 'Filter Hotel') {
        return this.bookings
      } else {
        return vm.bookings.filter(function (bookings) {
          return bookings.hotel === hotel
        })
      }
    }
  },
  data () {
    return {
      bookings: [],
      hotels: [],
      selectedHotel: 'Select a Hotel',
      filteredHotel: 'Filter Hotel',
      filteredFromParent: false,
      formattedFromDate: '',
      addBookingForm: {
        from: '',
        to: '',
        name: '',
        hotel: '',
        confirmed: []
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        from: '',
        to: '',
        name: '',
        hotel: '',
        confirmed: []
      }
    }
  },
  mounted: function () {
    if (this.$route.params.hotel !== undefined) {
      this.filteredFromParent = true
      this.filteredHotel = this.$route.params.hotel
    }
  },
  components: {
    alert: Alert,
    Datepicker
  },
  methods: {
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
    getBookings () {
      const path = 'http://localhost:5000/bookings'
      axios.get(path)
        .then((res) => {
          this.bookings = res.data.bookings
          this.bookings.forEach((booking) => {
            /* eslint-disable no-param-reassign */
            booking.from = moment(booking.from).format('DD/MM/YYYY')
            booking.to = moment(booking.to).format('DD/MM/YYYY')
          })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    },
    addBooking (payload) {
      const path = 'http://localhost:5000/bookings'
      axios.post(path, payload)
        .then(() => {
          this.getBookings()
          this.message = 'Booking added!'
          this.showMessage = true
          this.selectedHotel = 'Select a Hotel'
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBookings()
        })
    },
    initForm () {
      this.addBookingForm.from = ''
      this.addBookingForm.to = ''
      this.addBookingForm.name = ''
      this.addBookingForm.hotel = ''
      this.addBookingForm.confirmed = []
      this.editForm.id = ''
      this.editForm.from = ''
      this.editForm.to = ''
      this.editForm.name = ''
      this.editForm.hotel = ''
      this.editForm.read = []
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addBookingModal.hide()
      let confirmed = false
      this.addBookingForm.hotel = this.selectedHotel
      if (this.addBookingForm.confirmed[0]) confirmed = true
      const payload = {
        from: this.addBookingForm.from,
        to: this.addBookingForm.to,
        name: this.addBookingForm.name,
        hotel: this.addBookingForm.hotel,
        confirmed // property shorthand
      }
      this.addBooking(payload)
      this.initForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addBookingModal.hide()
      this.initForm()
    },
    editBooking (booking) {
      this.editForm = booking
      console.log(booking.from)
      const value = String(booking.from)
      console.log(value)
      console.log(moment(value, 'DD/MM/YYYY').format('DD/MM/YYYY'))
      /* eslint-disable no-param-reassign */
      this.editForm.from = moment(booking.from, 'DD/MM/YYYY')
      console.log(this.editForm.from)
      this.editForm.to = moment(booking.to, 'DD/MM/YYYY')
      console.log(booking.hotel)
      this.selectedHotel = booking.hotel
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editBookingModal.hide()
      let confirmed = false
      if (this.editForm.confirmed[0]) confirmed = true
      const payload = {
        from: this.editForm.from,
        to: this.editForm.to,
        name: this.editForm.name,
        hotel: this.editForm.hotel,
        confirmed
      }
      this.updateBooking(payload, this.editForm.id)
    },
    updateBooking (payload, bookingID) {
      const path = `http://localhost:5000/bookings/${bookingID}`
      axios.put(path, payload)
        .then(() => {
          this.getBookings()
          this.message = 'Booking updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBookings()
        })
    },
    onResetUpdate (evt) {
      evt.preventDefault()
      this.$refs.editBookingModal.hide()
      this.initForm()
      this.getBookings() // why?
    },
    removeBooking (bookingID) {
      const path = `http://localhost:5000/bookings/${bookingID}`
      axios.delete(path)
        .then(() => {
          this.getBookings()
          this.message = 'Booking removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBookings()
        })
    },
    onDeleteBooking (booking) {
      this.removeBooking(booking.id)
    },
    formatPicker () {
      const self = this
      const d = new Date(self.editForm.from)
      self.formatteFromDate = `${d.getUTCDate()}/${(d.getUTCMonth() + 1)}/${d.getUTCFullYear()}`
    },
    clearFilter () {
      this.filteredHotel = 'Filter Hotel'
      this.filteredFromParent = false
    }
  },
  created () {
    this.getBookings()
    this.getHotels()
  }
}
</script>
