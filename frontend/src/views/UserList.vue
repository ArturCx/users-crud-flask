<template>
  <div>
    <v-btn color="primary" class="mb-6 mt-5" @click="openCreateDialog">Create User</v-btn>
    <v-card class="elevation-1 rounded-lg">
      <v-data-table
        :headers="headers"
        :items="users"
        :hide-default-header="false"
      >
      <template v-slot:item.username="{ item }">
        <router-link :to="{ name: 'UserDetails', params: { id: item.id } }">
          {{ item.username }}
        </router-link>
      </template>
      <template v-slot:item.created_ts="{ item }">
      {{ convertTimestampToISO(item.created_ts) }}
      </template>
      <template v-slot:item.updated_ts="{ item }">
      {{ convertTimestampToISO(item.updated_ts) }}
      </template>
        <template v-slot:item.actions="{ item }">
          <v-btn icon @click="openEditDialog(item)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { User } from '../types/User'
import UserDialog from '../components/UserDialog.vue'

const users = ref<User[]>([])
const dialogVisible = ref(false)
const selectedUser = ref<User | null>(null)
const deleteConfirmation = ref(false)

const headers = [
  { title: 'Username', value: 'username' },
  { title: 'Roles', value: 'roles' },
  { title: 'Timezone', value: 'timezone' },
  { title: 'Is Active?', value: 'active' },
  { title: 'Last Updated At', value: 'updated_ts' },
  { title: 'Created At', value: 'created_ts' },
  { title: 'Actions', value: 'actions', sortable: false }
]

function convertTimestampToISO(timestamp: string | number): string {
  const timestampNumber = typeof timestamp === 'string' ? parseFloat(timestamp) : timestamp;
  const date = new Date(timestampNumber * 1000);
  return date.toISOString().replace('T', ' ').split('.')[0];  
}

onMounted(() => {
  fetchUsers()
})

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/users')
    users.value = response.data.sort((a: User, b: User) => Number(b.created_ts) - Number(a.created_ts))
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const openCreateDialog = () => {
  selectedUser.value = null
  dialogVisible.value = true
}

const openEditDialog = (user: User) => {
  selectedUser.value = user 
  dialogVisible.value = true
}

const saveUser = async (user: User) => {
  try {
    if (user.id) {
      // Atualiza o usuário existente
      await axios.put(`http://127.0.0.1:5000/users/${user.id}`, user)
    } else {
      // Cria um novo usuário
      const response = await axios.post('http://127.0.0.1:5000/users', user, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      user.id = response.data.id
    }
    fetchUsers()
    dialogVisible.value = false
  } catch (error) {
    console.error('Error saving user:', error)
  }
}

const confirmDelete = (user: User) => {
  selectedUser.value = user
  deleteConfirmation.value = true
}

const deleteUser = async () => {
  if (selectedUser.value) {
    try {
      await axios.delete(`http://127.0.0.1:5000/users/${selectedUser.value.id}`)
      fetchUsers()
      deleteConfirmation.value = false
    } catch (error) {
      console.error('Error deleting user:', error)
    }
  }
}
</script>
