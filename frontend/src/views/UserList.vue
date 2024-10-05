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
import { User } from '../types/User'
import UserDialog from '../components/UserDialog.vue'

const users = ref<User[]>([])
const dialogVisible = ref(false)
const selectedUser = ref<User | null>(null)
const deleteConfirmation = ref(false)

const headers = [
  { title: 'Username', key: 'username' },
  { title: 'Roles', key: 'roles' },
  { title: 'Timezone', key: 'timezone' },
  { title: 'Is Active?', key: 'isActive' },
  { title: 'Last Updated At', key: 'lastUpdatedAt' },
  { title: 'Created At', key: 'createdAt' },
  { title: 'Actions', key: 'actions', sortable: false }
]

onMounted(() => {
  // Fetch users from API
  // For now, we'll use mock data
  users.value = [
    {
      id: 1,
      username: 'john_doe',
      roles: ['User'],
      timezone: 'UTC',
      isActive: true,
      lastUpdatedAt: '2023-04-15T10:30:00Z',
      createdAt: '2023-04-01T09:00:00Z'
    },
    // Add more mock users here
  ]
})

const openCreateDialog = () => {
  selectedUser.value = null
  dialogVisible.value = true
}

const openEditDialog = (user: User) => {
  selectedUser.value = { ...user }
  dialogVisible.value = true
}

const saveUser = (user: User) => {
  if (user.id) {
    // Update existing user
    const index = users.value.findIndex(u => u.id === user.id)
    if (index !== -1) {
      users.value[index] = user
    }
  } else {
    // Create new user
    user.id = users.value.length + 1
    users.value.push(user)
  }
  dialogVisible.value = false
}

const confirmDelete = (user: User) => {
  selectedUser.value = user
  deleteConfirmation.value = true
}

const deleteUser = () => {
  if (selectedUser.value) {
    users.value = users.value.filter(u => u.id !== selectedUser.value?.id)
    deleteConfirmation.value = false
  }
}
</script>