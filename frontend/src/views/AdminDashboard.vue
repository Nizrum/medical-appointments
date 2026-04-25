<template>
	<div class="space-y-6">
		<div class="bg-white shadow rounded-lg p-6">
			<h1 class="text-2xl font-bold mb-2">Панель администратора</h1>
			<p class="text-gray-600">
				Добро пожаловать, {{ authStore.user?.full_name }}
			</p>
		</div>

		<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
			<div class="bg-white shadow rounded-lg p-6 text-center">
				<h3 class="text-lg font-semibold mb-2">Пользователи</h3>
				<router-link
					to="/admin/users"
					class="text-blue-600"
					>Управление пользователями →</router-link
				>
			</div>
			<div class="bg-white shadow rounded-lg p-6 text-center">
				<h3 class="text-lg font-semibold mb-2">Врачи</h3>
				<router-link
					to="/admin/doctors"
					class="text-blue-600"
					>Управление врачами →</router-link
				>
			</div>
			<div class="bg-white shadow rounded-lg p-6 text-center">
				<h3 class="text-lg font-semibold mb-2">Записи</h3>
				<router-link
					to="/admin/appointments"
					class="text-blue-600"
					>Управление записями →</router-link
				>
			</div>
			<div class="bg-white shadow rounded-lg p-6 text-center">
				<h3 class="text-lg font-semibold mb-2">Услуги</h3>
				<router-link
					to="/admin/services"
					class="text-blue-600"
					>Управление услугами →</router-link
				>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { useAuthStore } from "../stores/auth";

	const authStore = useAuthStore();
</script>
