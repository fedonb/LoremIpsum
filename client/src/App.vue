<template>
  <div id="app">
    <app-header></app-header>
    <section class="main-section section">
      <div class="container content">
        <router-view></router-view>
      </div>
    </section>
    <!-- <app-footer></app-footer> -->
  </div>
</template>
<script>
import AppHeader from '@/components/AppHeader.vue'
// import AppFooter from './AppFooter.vue'

export default {
  components: {
    'app-header': AppHeader
  }
}
</script>
<style>
#app {
  margin-top: 60px
}
</style>
