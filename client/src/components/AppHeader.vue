<template>
  <header class="bg-dark text-center text-lg-start">
    <div class="container">
      <b-navbar toggleable="lg" type="dark" class="navbar-horizontal">
        <!-- <b-navbar-brand href="#">PRIMARY COLOR</b-navbar-brand> -->

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-left">
            <b-nav-form>
                <li class="nav-item">
                  <router-link class="nav-link nav-link-icon" to="/hotels">
                    <span class="nav-link nav-link-inner--text">
                      Hotels
                    </span>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link nav-link-icon" to="/hotels2">
                    <span class="nav-link nav-link-inner--text">
                      Hotels2
                    </span>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link nav-link-icon" to="/bookings">
                    <span class="nav-link nav-link-inner--text">
                      Bookings
                    </span>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link class="nav-link nav-link-icon" to="/about">
                    <span class="nav-link nav-link-inner--text">
                      About
                    </span>
                  </router-link>
                </li>
                <li class="nav-item">
                  <router-link v-if="isAuthenticated" v-on:click.native="logout()" class="nav-link nav-link-icon" to="/">
                    <span class="nav-link nav-link-inner--text">
                      Logout
                    </span>
                  </router-link>
                  <router-link v-else class="nav-link nav-link-icon" to="/login">
                    <span class="nav-link nav-link-inner--text">
                      Login
                    </span>
                  </router-link>
                </li>
            </b-nav-form>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </header>
</template>
<style scoped>
.navbar-default {
    background-color: white;
    border-color: white;
}
</style>
<script>
export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    }
  }
}
</script>
