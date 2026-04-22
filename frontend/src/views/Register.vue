<template>
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="max-w-md w-full space-y-8">
			<div>
				<h2
					class="mt-6 text-center text-3xl font-extrabold text-gray-900">
					Создать новый аккаунт
				</h2>
			</div>
			<form
				class="mt-8 space-y-6"
				@submit.prevent="handleRegister">
				<div class="space-y-4">
					<div>
						<input
							v-model="fullName"
							type="text"
							required
							class="input-field"
							placeholder="Полное имя" />
					</div>
					<div>
						<input
							v-model="email"
							type="email"
							required
							class="input-field"
							placeholder="Адрес электронной почты" />
					</div>
					<div>
						<input
							v-model="phone"
							type="tel"
							class="input-field"
							placeholder="Телефон (необязательно)" />
					</div>
					<div>
						<input
							v-model="password"
							type="password"
							required
							class="input-field"
							placeholder="Пароль" />
					</div>
				</div>

				<div
					v-if="error"
					class="text-red-600 text-sm text-center">
					{{ error }}
				</div>

				<div>
					<button
						type="submit"
						class="btn-primary w-full">
						Зарегистрироваться
					</button>
				</div>

				<div class="text-center">
					<router-link
						to="/login"
						class="text-blue-600 hover:text-blue-500">
						Уже есть аккаунт? Войти
					</router-link>
				</div>
			</form>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue";
	import { useAuthStore } from "../stores/auth";
	import { useRouter } from "vue-router";

	const authStore = useAuthStore();
	const router = useRouter();
	const fullName = ref("");
	const email = ref("");
	const phone = ref("");
	const password = ref("");
	const error = ref("");

	const handleRegister = async () => {
		const result = await authStore.register({
			full_name: fullName.value,
			email: email.value,
			phone: phone.value || null,
			role: "patient",
			password: password.value,
		});

		if (result.success) {
			await authStore.login({
				email: email.value,
				password: password.value,
			});
			router.push("/dashboard");
		} else {
			error.value = result.error;
		}
	};
</script>
