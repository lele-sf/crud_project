<template>
  <v-container>
    <v-data-table-server
      :headers="headers"
      :items="formattedItems"
      :items-length="totalItems"
      :loading="loading"
      :disable-sort="true"
      @update:options="updateOptions"
    >
      <template #top>
        <v-toolbar flat>
          <v-toolbar-title>Projetos</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          />
          <v-spacer />
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template #activator="{ props }">
              <v-btn
                class="mb-2"
                color="primary"
                dark
                v-bind="props"
                @click="openCreateDialog"
              >
                Criar projeto
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ dialogTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="currentProject.title"
                        label="Nome"
                      />
                      <v-text-field
                        v-model="currentProject.description"
                        label="Descrição"
                      />
                      <v-select
                        v-model="currentProject.status"
                        :items="listStatus"
                        label="Status"
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
                  @click="closeDialog"
                >
                  Cancelar
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="saveProject"
                >
                  Salvar
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog
            v-model="dialogDelete"
            max-width="500px"
          >
            <v-card>
              <v-card-title class="text-h5 text-wrap">
                Tem certeza que você deseja deletar esse item?
              </v-card-title>
              <v-card-actions>
                <v-spacer />
                <v-btn
                  color="blue-darken-1"
                  variant="text"
                  @click="closeDeleteDialog"
                >
                  Cancelar
                </v-btn>
                <v-btn
                  color="blue-darken-1"
                  variant="text"
                  @click="deleteProjectConfirm"
                >
                  OK
                </v-btn>
                <v-spacer />
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>

      <template #[`item.title`]="{ item }">
        <RouterLink
          :to="item.boardLink"
          class="text-blue hover-underline"
        >
          {{ item.title }}
        </RouterLink>
      </template>

      <template #[`item.actions`]="{ item }">
        <v-icon
          class="me-2"
          size="small"
          @click="openEditDialog(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          size="small"
          @click="openDeleteDialog(item)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table-server>
  </v-container>
</template>

<script>
import { useDate } from 'vuetify'

export default {
	setup() {
    const date = useDate()
    const formatDate = (dateString) => {
      return date.format(dateString, 'keyboardDate')
    }
    return {
      formatDate
    }
  },
  data() {
		return {
			dialog: false,
			dialogDelete: false,
			isEditMode: false,
			headers: [
				{ title: 'Nome', key: 'title'},
				{ title: 'Descrição', key: 'description'},
				{ title: 'Status', key: 'status'},
				{ title: 'Criado em', key: 'created_at'},
				{ title: 'Ações', key: 'actions'}
			],
			serverItems: [],
			totalItems: 0,
			loading: true,
			currentProject: {
				id: null,
				title: '',
				description: '',
				status: ''
			},
			listStatus: ['pending', 'paused', 'doing', 'completed'],
			options: {
				page: 1,
			},
		};
 },
  computed: {
    dialogTitle() {
      return this.isEditMode ? 'Editar Projeto' : 'Novo Projeto';
    },
		formattedItems() {
      return this.serverItems.map(project => ({
        ...project,
        created_at: this.formatDate(project.created_at),
				boardLink: `/board/${project.id}`
      }));
    }
  },
  mounted() {
    this.loadItems(this.options)
  },
  methods: {
    loadItems({ page, itemsPerPage }) {
      const offset = (page - 1) * itemsPerPage;
      this.loading = true;

      this.$axios
        .get('/clients/1/projects', {
          params: {
            client_id: 1,
            offset,
            limit: itemsPerPage
          },
        })
        .then(({ data }) => {
          this.serverItems = data.projects;
          this.totalItems = data.total;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    openCreateDialog() {
      this.isEditMode = false;
      this.currentProject = { id: null, title: '', description: '', status: '' };
      this.dialog = true;
    },
    openEditDialog(project) {
      this.isEditMode = true;
      this.currentProject = { ...project };
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.currentProject = { id: null, title: '', description: '', status: '' };
    },
    saveProject() {
      if (this.isEditMode) {
        this.updateProject();
      } else {
        this.createProject();
      }
    },
    createProject() {
      this.$axios
        .post('/clients/1/projects', {
          client_id: 1,
          ...this.currentProject,
        })
        .then(() => {
          this.dialog = false;
          this.loadItems(this.options);
        })
        .catch((error) => {
          console.error('Erro salvando projeto:', error);
        });
    },
    updateProject() {
      this.$axios
        .patch(`/clients/1/projects/${this.currentProject.id}`, {
          client_id: 1,
          ...this.currentProject,
        })
        .then(() => {
          this.dialog = false;
          this.loadItems(this.options);
        })
        .catch((error) => {
          console.error('Erro atualizando projeto:', error);
        });
    },
    openDeleteDialog(project) {
      this.currentProject = { ...project };
      this.dialogDelete = true;
    },
    deleteProjectConfirm() {
      this.$axios
        .delete(`/clients/1/projects/${this.currentProject.id}`, {
          params: { client_id: 1 },
        })
        .then(() => {
          this.dialogDelete = false;
          this.loadItems(this.options);
        })
        .catch((error) => {
          console.error('Erro deletando o projeto:', error);
        });
    },
    closeDeleteDialog() {
      this.dialogDelete = false;
    },
    updateOptions(options) {
      this.options = options;
      this.loadItems(options);
    },
  },
}
</script>

<style scoped>
.hover-underline {
  text-decoration: none;
}
.hover-underline:hover {
  text-decoration: underline;
}
</style>
