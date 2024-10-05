<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>User Management</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Users</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
  //
</script>
