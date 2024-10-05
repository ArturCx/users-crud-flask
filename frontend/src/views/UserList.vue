<template>
  <div>
    <v-btn color="primary" class="mb-6 mt-5" @click="openCreateDialog">Create User</v-btn>
    <v-card class="elevation-1 rounded-lg">
      <v-data-table
        :headers="headers"
        :items="users"
      >
        <template v-slot:item.username="{ item }">
          <router-link :to="{ name: 'UserDetails', params: { id: item.id } }">
            {{ item.username }}
          </router-link>
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
  { text: 'Username', value: 'username' },
  { text: 'Roles', value: 'roles' },
  { text: 'Timezone', value: 'timezone' },
  { text: 'Is Active?', value: 'active' },
  { text: 'Last Updated At', value: 'updated_ts' },
  { text: 'Created At', value: 'created_ts' },
  { text: 'Actions', value: 'actions', sortable: false }
]

onMounted(() => {
  fetchUsers()
})

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/users')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const openCreateDialog = () => {
  selectedUser.value = null
  dialogVisible.value = true
}

const openEditDialog = (user: User) => {
  selectedUser.value = { ...user }
  dialogVisible.value = true
}

const saveUser = async (user: User) => {
  try {
    if (user.id) {
      // Atualiza o usuário existente
      await axios.put(`http://127.0.0.1:5000/users/${user.id}`, user)
    } else {
      // Cria um novo usuário
      const response = await axios.post('http://127.0.0.1:5000/users/', user)
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
