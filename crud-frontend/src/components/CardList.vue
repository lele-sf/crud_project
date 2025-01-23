<template>
  <v-container>
    <v-row>
      <v-col
        v-for="status in listStatus"
        :key="status"
        cols="12"
        md="3"
        class="d-flex px-2"
      >
        <v-sheet
          border="md"
          class="pa-5 text-white mx-auto w-100"
          color="#141518"
          :data-status="status"
        >
          <h4 class="text-h6 font-weight-medium mb-4 text-uppercase">
            {{ statusLabels[status] }}
          </h4>
          <draggable
            :list="filteredTasks(status)"
            group="tasks"
            @end="onTaskDrop"
          >
            <div
              v-for="task in filteredTasks(status)"
              :key="task.id"
              :data-task-id="task.id"
              style="cursor: pointer;"
              @click="openCardDetail(task)"
            >
              <v-card class="mb-2 py-4">
                <v-card-title>{{ task.title }}</v-card-title>
                <v-tooltip>
                  <template #activator="{ props }">
                    <v-avatar
                      v-bind="props"
                      class="position-absolute right-0 bottom-0"
                    >
                      <v-icon icon="mdi-account-circle" />
                    </v-avatar>
                  </template>
                  <span>Responsável: {{ task.assigned_to }}</span>
                </v-tooltip>
              </v-card>
            </div>
          </draggable>
          <v-divider class="mb-4" />
          <v-btn
            class="text-none"
            color="blue"
            size="large"
            variant="text"
            prepend-icon="$plus"
            @click="openCreateDialog(status)"
          >
            Criar item
          </v-btn>
        </v-sheet>
      </v-col>
    </v-row>

    <v-dialog
      v-model="dialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ dialogTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="currentTask.title"
                  label="Título"
                />
                <v-text-field
                  v-model="currentTask.description"
                  label="Descrição"
                />
                <v-text-field
                  v-model="currentTask.assigned_to"
                  label="Responsável"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue darken-1"
            text
            @click="close"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="saveTask"
          >
            Salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="detailDialog"
      max-width="600px"
    >
      <Card
        v-if="selectedTask"
        :task="selectedTask"
        :status-labels="statusLabels"
        @close="detailDialog = false"
        @edit-task="openEditDialog"
        @delete-task="deleteTask"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import { VueDraggableNext } from 'vue-draggable-next'
import Card from './Card.vue';

export default {
  components: {
    draggable: VueDraggableNext,
		Card
  },
  props: {
    tasks: {
      type: Array,
      required: true,
    },
		projectId: {
			type: String,
			required: true
		}
  },
	emits: ['update:tasks'],
  data() {
    return {
			dialog: false,
			detailDialog: false,
      selectedTask: null,
			isEditMode: false,
			currentTask: {
        title: '',
        description: '',
        status: '',
				assigned_to: ''
      },
      listStatus: ['pending', 'paused', 'doing', 'completed'],
      statusLabels: {
        pending: 'Não iniciado',
        paused: 'Em pausa',
        doing: 'Em progresso',
        completed: 'Concluído',
      },
    };
  },
	computed: {
    dialogTitle() {
      return this.isEditMode ? 'Editar Item' : 'Novo Item';
    }
  },
  methods: {
    filteredTasks(status) {
      return this.tasks.filter(task => task.status === status);
    },
    onTaskDrop(event) {
      const { item, to } = event;
      const taskId = item.getAttribute('data-task-id');
      const newStatus = to.closest('[data-status]').getAttribute('data-status');
      const task = this.tasks.find(task => task.id === parseInt(taskId));

      if (task && task.status !== newStatus) {
        task.status = newStatus;
        this.$axios
          .patch(`/projects/${this.projectId}/tasks/${task.id}`, { status: newStatus })
          .then(() => {
            this.$emit('update:tasks', this.tasks);
          })
          .catch((error) => {
            console.error('Erro atualizando o status da task:', error);
          });
      }
    },
		openCreateDialog(status) {
      this.isEditMode = false;
      this.currentTask = { title: '', description: '', status, assigned_to: '' };
      this.dialog = true;
    },
    openEditDialog(task) {
      this.isEditMode = true;
      this.currentTask = { ...task };
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.currentTask = { title: '', description: '', status: '', assigned_to: '' };
    },
    saveTask() {
      if (this.isEditMode) {
        this.updateTask();
      } else {
        this.createTask();
      }
    },
    createTask() {
      this.$axios
        .post(`/projects/${this.projectId}/tasks`, {
          ...this.currentTask,
        })
        .then(({ data }) => {
          this.$emit('update:tasks', [...this.tasks, data]);
          this.dialog = false;
        })
        .catch((error) => {
          console.error('Erro criando a tarefa:', error);
        });
    },
    updateTask() {
      this.$axios
        .patch(`/projects/${this.projectId}/tasks/${this.currentTask.id}`, {
          ...this.currentTask,
        })
        .then(({ data }) => {
          this.$emit('update:tasks', this.tasks.map(task => task.id === data.id ? data : task));
          this.dialog = false;
        })
        .catch((error) => {
          console.error('Erro atualizando a tarefa:', error);
        });
    },
    deleteTask(task) {
      this.$axios
        .delete(`/projects/${this.projectId}/tasks/${task.id}`)
        .then(() => {
          this.$emit('update:tasks', this.tasks.filter(t => t.id !== task.id));
          this.detailDialog = false;
        })
        .catch((error) => {
          console.error('Erro deletando a tarefa:', error);
        });
    },
    openCardDetail(task) {
      this.selectedTask = task;
      this.detailDialog = true;
    },
  },
};
</script>
