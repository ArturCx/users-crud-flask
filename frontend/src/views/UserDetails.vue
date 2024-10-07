<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <div v-if="user" class="text-center">
          
          <v-card class="mb-4 rounded-lg" max-width="500" width="100%">
            <v-list>
              <h1 class="mb-4">Details of {{ user.username }}</h1>
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
                <v-list-item-subtitle>{{ user.active ? 'Yes' : 'No' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Last Updated At</v-list-item-title>
                <v-list-item-subtitle>{{ convertTimestampToISO(user.updated_ts) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Created At</v-list-item-title>
                <v-list-item-subtitle>{{ convertTimestampToISO(user.created_ts) }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>

            <v-card-actions class="justify-center">
              <v-btn color="primary" class="mr-2" @click="openEditDialog(user)">Edit</v-btn>
              <v-btn color="error" @click="confirmDelete">Delete</v-btn>
            </v-card-actions>
          </v-card>

          <user-dialog
            v-model="dialogVisible"
            :user="selectedUser"
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
import axios from 'axios'
import { User } from '../types/User'
import UserDialog from '../components/UserDialog.vue'

const router = useRouter()
const route = useRoute()
const user = ref<User | null>(null)
const selectedUser = ref<User | null>(null)
const dialogVisible = ref(false)
const deleteConfirmation = ref(false)

function convertTimestampToISO(timestamp: string | number): string {
  const timestampNumber = typeof timestamp === 'string' ? parseFloat(timestamp) : timestamp;
  const date = new Date(timestampNumber * 1000);
  return date.toISOString().replace('T', ' ').split('.')[0];  
}

const fetchUserDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/users/${route.params.id}`)
    user.value = response.data
  } catch (error) {
    console.error('Error fetching user details:', error)
    router.push({ name: 'UserList' })
  }
}

onMounted(() => {
  fetchUserDetails()
})

const openEditDialog = (user: User) => {
  selectedUser.value = { ...user }
  dialogVisible.value = true
}

const saveUser = async (updatedUser: User) => {
  try {
    await axios.put(`http://127.0.0.1:5000/users/${updatedUser.id}`, updatedUser)
    user.value = { ...updatedUser }
    dialogVisible.value = false
  } catch (error) {
    console.error('Error updating user:', error)
  }
}

const confirmDelete = () => {
  deleteConfirmation.value = true
}

const deleteUser = async () => {
  try {
    await axios.delete(`http://127.0.0.1:5000/users/${user.value?.id}`)
    router.push({ name: 'UserList' })
  } catch (error) {
    console.error('Error deleting user:', error)
  }
}
</script>
