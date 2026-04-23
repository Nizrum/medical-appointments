<template>
	<div class="border rounded-lg p-4 hover:shadow-md transition">
		<div class="flex justify-between items-start">
			<div class="flex-1">
				<h3 class="font-semibold">
					{{
						isDoctor
							? appointment.patient_name || "Пациент"
							: appointment.doctor_name || "Врач"
					}}
				</h3>
				<p
					v-if="!isDoctor && appointment.doctor_specialization"
					class="text-sm text-gray-600">
					{{ appointment.doctor_specialization }}
				</p>
				<p
					v-if="appointment.doctor_cabinet"
					class="text-sm text-gray-600">
					Кабинет: {{ appointment.doctor_cabinet }}
				</p>
				<p class="text-sm text-gray-600">
					Дата: {{ formatDate(appointment.time_start) }}
				</p>
				<p class="text-sm text-gray-600">
					Время: {{ formatTime(appointment.time_start) }} -
					{{ formatTime(appointment.time_end) }}
				</p>
				<p
					v-if="appointment.service_name"
					class="text-sm text-gray-600">
					Услуга: {{ appointment.service_name }}
				</p>
				<p
					v-if="appointment.complaints"
					class="text-sm text-gray-600">
					Жалобы: {{ appointment.complaints }}
				</p>
				<p
					v-if="appointment.patient_phone"
					class="text-sm text-gray-600">
					Телефон: {{ appointment.patient_phone }}
				</p>
				<p class="text-sm mt-2">
					Статус:
					<span
						:class="statusClass"
						class="font-semibold">
						{{ statusText }}
					</span>
				</p>
			</div>
			<div class="flex space-x-2">
				<button
					v-if="
						showCancel &&
						(appointment.status === 'scheduled' ||
							appointment.status === 'confirmed')
					"
					@click="$emit('cancel')"
					class="btn-danger text-sm px-3 py-1">
					Отменить
				</button>
				<button
					v-if="showComplete && appointment.status === 'confirmed'"
					@click="$emit('complete')"
					class="btn-primary text-sm px-3 py-1">
					Завершить
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { computed } from "vue";
	import { formatDate, formatTime } from "../utils/date";

	const props = defineProps({
		appointment: {
			type: Object,
			required: true,
		},
		showCancel: {
			type: Boolean,
			default: false,
		},
		showComplete: {
			type: Boolean,
			default: false,
		},
		isDoctor: {
			type: Boolean,
			default: false,
		},
	});

	defineEmits(["cancel", "complete"]);

	const statusText = computed(() => {
		const statuses = {
			scheduled: "Запланирована",
			confirmed: "Подтверждена",
			completed: "Завершена",
			cancelled: "Отменена",
			available: "Свободно",
		};
		return (
			statuses[props.appointment.status] ||
			props.appointment.status ||
			"Неизвестно"
		);
	});

	const statusClass = computed(() => {
		const classes = {
			scheduled: "text-blue-600",
			confirmed: "text-green-600",
			completed: "text-gray-600",
			cancelled: "text-red-600",
			available: "text-gray-500",
		};
		return classes[props.appointment.status] || "text-gray-600";
	});
</script>
