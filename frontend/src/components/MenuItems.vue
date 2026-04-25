<template>
	<div>
		<template v-if="authStore.userRole === 'patient'">
			<router-link
				to="/services"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Все услуги
			</router-link>
			<router-link
				to="/doctors"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Записаться к врачу
			</router-link>
			<router-link
				to="/my-appointments"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Мои записи
			</router-link>
		</template>

		<template v-if="authStore.userRole === 'doctor'">
			<router-link
				to="/doctor-dashboard"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Панель врача
			</router-link>
			<router-link
				to="/doctor-schedule"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Расписание
			</router-link>
		</template>

		<template v-if="authStore.userRole === 'admin'">
			<router-link
				to="/admin"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Панель администратора
			</router-link>
			<router-link
				to="/admin/users"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Пользователи
			</router-link>
			<router-link
				to="/admin/doctors"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Врачи
			</router-link>
			<router-link
				to="/admin/appointments"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Записи
			</router-link>
			<router-link
				to="/admin/services"
				class="hover:text-blue-200 block lg:inline-block lg:ml-4"
				@click="$emit('click')">
				Услуги
			</router-link>
		</template>
	</div>
</template>

<script setup>
	import { useAuthStore } from "../stores/auth";

	const authStore = useAuthStore();

	defineEmits(["click"]);
</script>
