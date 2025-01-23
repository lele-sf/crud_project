<template>
  <v-card rounded="lg">
    <v-card-title>
      <div class="d-flex justify-space-between align-center">
        <div class="text-h5 ps-2">
          {{ task.title }}
        </div>
        <div>
          <v-btn
            icon="mdi-pencil"
            variant="text"
            @click="$emit('edit-task', task)"
          />
          <v-btn
            icon="mdi-delete"
            variant="text"
            @click="$emit('delete-task', task)"
          />
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="$emit('close')"
          />
        </div>
      </div>
      <v-chip
        label
        size="small"
        color="primary"
      >
        {{ statusLabels[task.status] }}
      </v-chip>
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <p class="text-h5">
            Descrição
          </p>
          <p>{{ task.description }}</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <p class="text-h5">
            Responsável
          </p>
          <p>{{ task.assigned_to }}</p>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    task: {
      type: Object,
      required: true,
    },
    statusLabels: {
      type: Object,
      required: true,
    },
  },
  emits: ['close', 'edit-task', 'delete-task'],
};
</script>

