<template>
<div class="content">
  <div class="row">
    <div class="col-sm-10">
      <b-form class="authenticate" @submit.prevent="authenticate">
        <h1>Log in</h1>
        <hr><br><br>
        <b-form-group id="form-email-group"
                    label="Email:"
                    label-for="form-email-input">
        <!-- <label>Email</label> -->
          <b-form-input required v-model="email"
                        type="text"
                        placeholder="Email"
                        autocomplete="on">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group"
                    label="Password:"
                    label-for="form-password-input">
        <!-- <label>Password</label> -->
          <b-form-input required v-model="password"
                        type="password"
                        placeholder="Password"
                        autocomplete="on">
          </b-form-input>
        </b-form-group>
        <hr/>
        <b-button-group>
          <b-button type="submit">Login</b-button>
        </b-button-group>
      </b-form>
    </div>
  </div>
</div>
</template>
<script>
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    authenticate () {
      const logemail = this.email
      const logpassword = this.password
      this.$store.dispatch('login', { email: logemail, password: logpassword })
        .then(() => this.$router.push('/'))
        .catch((err) => console.log(err))
      // this.$store.dispatch('login', { logemail, logpassword })
      //   .then(() => this.$router.push('/'))
      //   .catch((err) => console.log(err));
    }
  }
}
</script>
