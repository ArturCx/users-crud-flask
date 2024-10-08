<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.username"
                  label="Username"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.password"
                  label="Password"
                  :rules="[rules.required]"
                  required
                  type="password"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedUser.roles"
                  :items="['user', 'admin', 'moderator']"
                  label="Roles"
                  multiple
                  chips
                  :rules="[rules.required]"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.timezone"
                  label="Timezone"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editedUser.active"
                  label="Is Active?"
                  required
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" @click="close">Cancel</v-btn>
        <v-btn color="blue-darken-1" @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { User } from '../types/User'
import { VForm } from 'vuetify/components/VForm';

const props = defineProps<{
  modelValue: boolean,
  user: User | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'save', user: User): void
}>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Validação dos campos
const form = ref<InstanceType<typeof VForm> | null>(null)
const valid = ref(false)

const rules = {
  required: (value: string) => !!value || 'Field is required'
}

const editedUser = ref<User>({
  id: 0,
  username: '',
  password: '',
  roles: [],
  timezone: '',
  active: true,
  updated_ts: '',
  created_ts: ''
})

const formTitle = computed(() => {
  return editedUser.value.id ? 'Edit User' : 'New User'
})

watch(() => props.user, (newUser) => {
  if (newUser) {
    editedUser.value = { ...newUser }
  } else {
    editedUser.value = {
      id: 0,
      username: '',
      password: '',
      roles: [],
      timezone: '',
      active: true,
      updated_ts: '',
      created_ts: ''
    }
  }
})

const close = () => {
  dialog.value = false
}

const save = () => {
  // Verifica se o formulário é válido antes de enviar
  form.value?.validate().then((result) => {
    if (result) {
      emit('save', editedUser.value)
      close()
    }
  })
}
</script>
