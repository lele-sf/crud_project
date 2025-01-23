<template>
  <v-app-bar
    class="px-3"
    density="compact"
  >
    <template v-if="$vuetify.display.smAndDown">
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
      />
    </template>

    <v-app-bar-title
      style="cursor: pointer;"
      @click="navigate('Projetos')"
    >
      Jello
    </v-app-bar-title>

    <template v-if="$vuetify.display.mdAndUp">
      <v-tabs color="grey-darken-2">
        <v-tab
          v-for="link in links"
          :key="link"
          :text="link"
          @click="navigate(link)"
        />
      </v-tabs>
      <v-btn
        variant="outlined"
        color="primary"
        @click="createNewBoard"
      >
        Criar
      </v-btn>
    </template>

    <v-spacer />

    <div v-show="$vuetify.display.mdAndUp">
      <v-btn icon="mdi-magnify" />
      <v-btn icon="mdi-bell-outline" />
      <v-btn icon="mdi-cog" />
    </div>

    <v-menu
      min-width="200px"
      rounded
    >
      <template #activator="{ props }">
        <v-btn
          icon
          v-bind="props"
        >
          <v-avatar
            color="info"
            size="small"
          >
            <v-icon icon="mdi-account-circle" />
          </v-avatar>
        </v-btn>
      </template>
      <v-card>
        <v-card-text>
          <div class="mx-auto text-center">
            <v-avatar color="info">
              <v-icon icon="mdi-account-circle" />
            </v-avatar>
            <h3>{{ user.company }}</h3>
            <p class="text-caption mt-1">
              {{ user.email }}
            </p>
            <v-divider class="my-3" />
            <v-btn
              variant="text"
              rounded
            >
              Editar Conta
            </v-btn>
            <v-divider class="my-3" />
            <v-btn
              variant="text"
              rounded
            >
              Logout
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-menu>
  </v-app-bar>

  <v-navigation-drawer
    v-model="drawer"
    temporary
  >
    <v-list>
      <v-list-item
        v-for="link in links"
        :key="link"
        @click.stop="navigate(link)"
      >
        <v-list-item-title>{{ link }}</v-list-item-title>
      </v-list-item>
      <v-list-item @click="createNewBoard">
        <v-list-item-title>
          <v-btn
            variant="outlined"
            color="primary"
            @click="createNewBoard"
          >
            Criar
          </v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
	export default {
	data() {
		return {

			drawer: false,
			links: ['Projetos', 'Recente', 'Favoritos'],
			user: {
					company: '',
					email: '',
				},
			};
		},
	mounted() {
		this.fetchClientInfo();
	},
	methods: {
		navigate(link) {
	    if (link === 'Projetos') {
				this.$router.push('/')
			} else {
				console.log(`${link} clicked`)
			}
		},
		createNewBoard() {
  		console.log('Create New Board clicked')
		},
		fetchClientInfo() {
      this.$axios.get('/clients/1').then(response => {
				const client = response.data;
        this.user = {
          company: client.company,
          email: client.email,
        };
      }).catch(error => {
        console.error('Não foi possível carregar o cliente.', error);
      });
    },
  },
};
</script>
