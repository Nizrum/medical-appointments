<template>
	<nav class="bg-blue-600 text-white shadow-lg relative">
		<div class="container mx-auto px-4">
			<div class="flex justify-between items-center py-4">
				<div class="text-xl font-bold">
					<router-link :to="homeRoute">Система записи</router-link>
				</div>

				<button
					@click="mobileMenuOpen = !mobileMenuOpen"
					class="lg:hidden flex flex-col items-center justify-center w-10 h-10 rounded hover:bg-blue-700 transition">
					<span class="block w-6 h-0.5 bg-white mb-1.5"></span>
					<span class="block w-6 h-0.5 bg-white mb-1.5"></span>
					<span class="block w-6 h-0.5 bg-white"></span>
				</button>

				<div class="hidden lg:flex lg:items-center lg:space-x-4">
					<MenuItems @click="mobileMenuOpen = false" />
					<button
						@click="logout"
						class="hover:text-blue-200 ml-4">
						Выйти
					</button>
				</div>
			</div>

			<div
				v-if="mobileMenuOpen"
				class="lg:hidden py-4 border-t border-blue-500">
				<div class="flex flex-col space-y-3">
					<MenuItems @click="mobileMenuOpen = false" />
					<button
						@click="logout"
						class="text-left hover:text-blue-200 py-2">
						Выйти
					</button>
				</div>
			</div>
		</div>
	</nav>
</template>

<script setup>
	import { computed, ref } from "vue";
	import { useAuthStore } from "../stores/auth";
	import { useRouter } from "vue-router";
	import MenuItems from "./MenuItems.vue";

	const authStore = useAuthStore();
	const router = useRouter();
	const mobileMenuOpen = ref(false);

	const homeRoute = computed(() => {
		if (authStore.userRole === "admin") return "/admin";
		if (authStore.userRole === "doctor") return "/doctor-dashboard";
		return "/dashboard";
	});

	const logout = () => {
		authStore.logout();
		router.push("/login");
	};
</script>
