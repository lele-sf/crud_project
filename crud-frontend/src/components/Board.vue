<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs" />
    <div v-if="loading">
      Carregando...
    </div>
    <div v-else-if="error">
      {{ error }}
    </div>
    <div v-else>
      <h1>{{ project.title }}</h1>
      <CardList
        :tasks="tasks"
        :project-id="projectId"
        @update:tasks="handleUpdateTasks"
      />
    </div>
  </v-container>
</template>

<script>
import CardList from '@/components/CardList.vue'

export default {
  components: {
    CardList,
  },
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      error: null,
      project: null,
      tasks: [],
      breadcrumbs: [
        { title: 'Projetos', href: '/' },
        { title: 'Carregando...', disabled: true },
      ],
    };
  },
  mounted() {
    this.fetchProject();
    this.fetchTasks();
  },
  methods: {
    fetchProject() {
      this.loading = true;

      this.$axios
        .get(`/clients/1/projects/${this.projectId}`)
        .then(({ data }) => {
          this.project = data;
          this.breadcrumbs[1].title = data.title;
        })
        .catch((error) => {
          console.error('Não foi possível carregar o projeto.', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchTasks() {
      this.loading = true;

      this.$axios
        .get(`/projects/${this.projectId}/tasks/`)
        .then(({ data }) => {
          this.tasks = data.tasks;
        })
        .catch((error) => {
          console.error('Não foi possível carregar as tarefas.', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handleUpdateTasks(updatedTasks) {
      this.tasks = updatedTasks;
    },
  },
};
</script>
