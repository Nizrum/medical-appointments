<template>
	<div class="bg-white shadow rounded-lg p-6">
		<div class="flex justify-between items-center mb-6">
			<h1 class="text-2xl font-bold">Управление услугами</h1>
			<button
				@click="openCreateModal"
				class="btn-primary">
				Добавить услугу
			</button>
		</div>

		<div
			v-if="adminStore.loading"
			class="text-center py-8">
			Загрузка...
		</div>
		<div
			v-else
			class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			<div
				v-for="service in adminStore.services"
				:key="service.id"
				class="border rounded-lg p-4 hover:shadow-lg transition">
				<div class="flex justify-between items-start mb-3">
					<h3 class="text-lg font-semibold">{{ service.name }}</h3>
					<div class="space-x-2">
						<button
							@click="openEditModal(service)"
							class="text-blue-600 hover:text-blue-900">
							✏️
						</button>
						<button
							@click="deleteService(service.id)"
							class="text-red-600 hover:text-red-900">
							🗑️
						</button>
					</div>
				</div>
				<p
					v-if="service.description"
					class="text-gray-600 text-sm mb-2">
					{{ service.description }}
				</p>
				<p
					v-if="service.price"
					class="text-gray-700 font-semibold">
					Цена: {{ service.price }} ₽
				</p>
				<p class="text-gray-600 text-sm">
					Длительность: {{ service.duration }} мин
				</p>
			</div>
		</div>

		<!-- Модальное окно создания/редактирования услуги -->
		<div
			v-if="showServiceModal"
			class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
			<div
				class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
				<h3 class="text-lg font-medium mb-4">
					{{
						editingService
							? "Редактировать услугу"
							: "Добавить услугу"
					}}
				</h3>

				<div class="space-y-4">
					<div>
						<label
							class="block text-sm font-medium text-gray-700 mb-2"
							>Название *</label
						>
						<input
							v-model="serviceForm.name"
							type="text"
							class="input-field"
							required />
					</div>

					<div>
						<label
							class="block text-sm font-medium text-gray-700 mb-2"
							>Описание</label
						>
						<textarea
							v-model="serviceForm.description"
							rows="3"
							class="input-field"></textarea>
					</div>

					<div>
						<label
							class="block text-sm font-medium text-gray-700 mb-2"
							>Цена (₽)</label
						>
						<input
							v-model="serviceForm.price"
							type="number"
							class="input-field" />
					</div>

					<div>
						<label
							class="block text-sm font-medium text-gray-700 mb-2"
							>Длительность (мин)</label
						>
						<input
							v-model="serviceForm.duration"
							type="number"
							class="input-field"
							required />
					</div>
				</div>

				<div class="flex justify-end space-x-3 mt-6">
					<button
						@click="showServiceModal = false"
						class="btn-secondary">
						Отмена
					</button>
					<button
						@click="saveService"
						class="btn-primary">
						Сохранить
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useAdminStore } from "../stores/admin";

	const adminStore = useAdminStore();
	const showServiceModal = ref(false);
	const editingService = ref(null);

	const serviceForm = ref({
		name: "",
		description: "",
		price: null,
		duration: 30,
	});

	const openCreateModal = () => {
		editingService.value = null;
		serviceForm.value = {
			name: "",
			description: "",
			price: null,
			duration: 30,
		};
		showServiceModal.value = true;
	};

	const openEditModal = (service) => {
		editingService.value = service;
		serviceForm.value = {
			name: service.name,
			description: service.description || "",
			price: service.price,
			duration: service.duration,
		};
		showServiceModal.value = true;
	};

	const saveService = async () => {
		if (!serviceForm.value.name) {
			alert("Введите название услуги");
			return;
		}

		let result;
		if (editingService.value) {
			result = await adminStore.updateService(
				editingService.value.id,
				serviceForm.value,
			);
		} else {
			result = await adminStore.createService(serviceForm.value);
		}

		if (result.success) {
			showServiceModal.value = false;
			alert(
				editingService.value ? "Услуга обновлена" : "Услуга создана",
			);
		} else {
			alert(result.error);
		}
	};

	const deleteService = async (serviceId) => {
		if (confirm("Удалить услугу?")) {
			const result = await adminStore.deleteService(serviceId);
			if (result.success) {
				alert("Услуга удалена");
			} else {
				alert(result.error);
			}
		}
	};

	onMounted(async () => {
		await adminStore.getServices();
	});
</script>
