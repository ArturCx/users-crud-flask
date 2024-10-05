<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <div v-if="user" class="text-center">
          <h1 class="mb-4">Details of {{ user.username }}</h1>
          <v-card class="mb-4 rounded-lg" max-width="500" width="100%">
            <v-list>
              <v-list-item>
                <v-list-item-title>Username</v-list-item-title>
                <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Roles</v-list-item-title>
                <v-list-item-subtitle>{{ user.roles.join(', ') }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Timezone</v-list-item-title>
                <v-list-item-subtitle>{{ user.timezone }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Is Active?</v-list-item-title>
                <v-list-item-subtitle>{{ user.isActive ? 'Yes' : 'No' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Last Updated At</v-list-item-title>
                <v-list-item-subtitle>{{ user.lastUpdatedAt }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Created At</v-list-item-title>
                <v-list-item-subtitle>{{ user.createdAt }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <v-btn color="primary" class="mr-2" @click="openEditDialog">Edit</v-btn>
          <v-btn color="error" @click="confirmDelete">Delete</v-btn>

          <user-dialog
            v-model="dialogVisible"
            :user="user"
            @save="saveUser"
          ></user-dialog>

          <v-dialog v-model="deleteConfirmation" max-width="300">
            <v-card class="rounded-lg">
              <v-card-title>Confirm Delete</v-card-title>
              <v-card-text>Are you sure you want to delete this user?</v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="deleteConfirmation = false">Cancel</v-btn>
                <v-btn color="error" @click="deleteUser">Delete</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { User } from '../types/User'
  import UserDialog from '../components/UserDialog.vue'
  
  const router = useRouter()
  const route = useRoute()
  const user = ref<User | null>(null)
  const dialogVisible = ref(false)
  const deleteConfirmation = ref(false)
  
  onMounted(() => {
    // Fetch user details from API
    // For now, we'll use mock data
    user.value = {
      id: Number(route.params.id),
      username: 'john_doe',
      roles: ['User'],
      timezone: 'UTC',
      isActive: true,
      lastUpdatedAt: '2023-04-15T10:30:00Z',
      createdAt: '2023-04-01T09:00:00Z'
    }
  })
  
  const openEditDialog = () => {
    dialogVisible.value = true
  }
  
  const saveUser = (updatedUser: User) => {
    user.value = updatedUser
    dialogVisible.value = false
  }
  
  const confirmDelete = () => {
    deleteConfirmation.value = true
  }
  
  const deleteUser = () => {
    // Delete user logic here
    // For now, we'll just navigate back to the user list
    router.push({ name: 'UserList' })
  }
  </script>