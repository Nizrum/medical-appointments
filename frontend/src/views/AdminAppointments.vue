<template>
	<div class="bg-white shadow rounded-lg p-6">
		<h1 class="text-2xl font-bold mb-6">Управление записями</h1>

		<!-- Фильтры -->
		<div class="grid md:grid-cols-4 gap-4 mb-6">
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Врач</label
				>
				<select
					v-model="filters.doctor_id"
					class="input-field"
					@change="applyFilters">
					<option value="">Все врачи</option>
					<option
						v-for="doctor in adminStore.doctors"
						:key="doctor.id"
						:value="doctor.id">
						{{ doctor.full_name }}
					</option>
				</select>
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Статус</label
				>
				<select
					v-model="filters.status"
					class="input-field"
					@change="applyFilters">
					<option value="">Все статусы</option>
					<option value="scheduled">Запланирована</option>
					<option value="confirmed">Подтверждена</option>
					<option value="completed">Завершена</option>
					<option value="cancelled">Отменена</option>
				</select>
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Дата от</label
				>
				<input
					v-model="filters.start_date"
					type="date"
					class="input-field"
					@change="applyFilters" />
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Дата до</label
				>
				<input
					v-model="filters.end_date"
					type="date"
					class="input-field"
					@change="applyFilters" />
			</div>
		</div>

		<div
			v-if="adminStore.loading"
			class="text-center py-8">
			Загрузка...
		</div>
		<div
			v-else-if="adminStore.appointments.length === 0"
			class="text-center py-8 text-gray-500">
			Нет записей
		</div>
		<div
			v-else
			class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Пациент
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Врач
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Дата
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Время
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Услуга
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Статус
						</th>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
							Действия
						</th>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					<tr
						v-for="appointment in adminStore.appointments"
						:key="appointment.id">
						<td class="px-6 py-4">
							<div class="font-medium">
								{{ appointment.patient_name || "—" }}
							</div>
							<div class="text-sm text-gray-500">
								{{ appointment.patient_phone || "—" }}
							</div>
						</td>
						<td class="px-6 py-4">
							<div>{{ appointment.doctor_name || "—" }}</div>
							<div class="text-sm text-gray-500">
								{{ appointment.doctor_specialization || "—" }}
							</div>
						</td>
						<td class="px-6 py-4">
							{{ formatDate(appointment.time_start) }}
						</td>
						<td class="px-6 py-4">
							{{ formatTime(appointment.time_start) }} -
							{{ formatTime(appointment.time_end) }}
						</td>
						<td class="px-6 py-4">
							{{ appointment.service_name || "—" }}
						</td>
						<td class="px-6 py-4">
							<span
								:class="statusClass(appointment.status)"
								class="px-2 py-1 text-xs font-semibold rounded-full">
								{{ statusText(appointment.status) }}
							</span>
						</td>
						<td class="px-6 py-4 whitespace-nowrap">
							<button
								v-if="appointment.status === 'scheduled'"
								@click="confirmAppointment(appointment.id)"
								class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 mr-2 text-sm">
								Подтвердить
							</button>
							<button
								@click="openRescheduleModal(appointment)"
								class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 text-sm">
								Перенести
							</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- Модальное окно переноса записи -->
		<div
			v-if="showRescheduleModal"
			class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
			<div
				class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
				<h3 class="text-lg font-medium mb-4">Перенос записи</h3>
				<p class="mb-2">
					Пациент: {{ selectedAppointment?.patient_name }}
				</p>
				<p class="mb-4">
					Врач: {{ selectedAppointment?.doctor_name }}
				</p>

				<div class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2"
						>Новая дата</label
					>
					<input
						v-model="newDate"
						type="date"
						class="input-field"
						@change="loadSlotsForReschedule" />
				</div>

				<div
					v-if="availableSlots.length > 0"
					class="mb-4">
					<label class="block text-sm font-medium text-gray-700 mb-2"
						>Новое время</label
					>
					<select
						v-model="selectedSlotId"
						class="input-field">
						<option value="">Выберите время</option>
						<option
							v-for="slot in availableSlots"
							:key="slot.id"
							:value="slot.id">
							{{ formatTime(slot.time_start) }}
						</option>
					</select>
				</div>

				<div
					v-else-if="newDate"
					class="text-center text-gray-500 mb-4">
					Нет доступных слотов на эту дату
				</div>

				<div class="flex justify-end space-x-3">
					<button
						@click="showRescheduleModal = false"
						class="btn-secondary">
						Отмена
					</button>
					<button
						@click="rescheduleAppointment"
						:disabled="!selectedSlotId"
						class="btn-primary">
						Перенести
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useAdminStore } from "../stores/admin";
	import { formatDate, formatTime } from "../utils/date";
	import api from "../services/api";

	const adminStore = useAdminStore();
	const filters = ref({
		doctor_id: "",
		status: "",
		start_date: "",
		end_date: "",
	});
	const showRescheduleModal = ref(false);
	const selectedAppointment = ref(null);
	const newDate = ref("");
	const selectedSlotId = ref("");
	const availableSlots = ref([]);

	const statusText = (status) => {
		const statuses = {
			scheduled: "Запланирована",
			confirmed: "Подтверждена",
			completed: "Завершена",
			cancelled: "Отменена",
		};
		return statuses[status] || status;
	};

	const statusClass = (status) => {
		const classes = {
			scheduled: "bg-yellow-100 text-yellow-800",
			confirmed: "bg-green-100 text-green-800",
			completed: "bg-blue-100 text-blue-800",
			cancelled: "bg-red-100 text-red-800",
		};
		return classes[status] || "bg-gray-100 text-gray-800";
	};

	const applyFilters = () => {
		adminStore.getAllAppointments(filters.value);
	};

	const confirmAppointment = async (appointmentId) => {
		if (confirm("Подтвердить запись?")) {
			const result = await adminStore.confirmAppointment(appointmentId);
			if (result.success) {
				alert("Запись подтверждена");
				await applyFilters();
			} else {
				alert(result.error);
			}
		}
	};

	const openRescheduleModal = (appointment) => {
		selectedAppointment.value = appointment;
		newDate.value = "";
		selectedSlotId.value = "";
		availableSlots.value = [];
		showRescheduleModal.value = true;
	};

	const loadSlotsForReschedule = async () => {
		if (!newDate.value || !selectedAppointment.value) return;

		try {
			const response = await api.get(
				`/patients/doctors/${selectedAppointment.value.doctor_id}/slots`,
				{
					params: { date: newDate.value },
				},
			);
			availableSlots.value = response.data || [];
		} catch (error) {
			console.error("Failed to load slots:", error);
			availableSlots.value = [];
		}
	};

	const rescheduleAppointment = async () => {
		if (!selectedSlotId.value) {
			alert("Выберите новое время");
			return;
		}

		const result = await adminStore.rescheduleAppointment(
			selectedAppointment.value.id,
			selectedSlotId.value,
		);

		if (result.success) {
			showRescheduleModal.value = false;
			alert("Запись перенесена");
			await applyFilters();
		} else {
			alert(result.error);
		}
	};

	onMounted(async () => {
		await Promise.all([
			adminStore.getAllAppointments(),
			adminStore.getDoctors(),
		]);
	});
</script>
