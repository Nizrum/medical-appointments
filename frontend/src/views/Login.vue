<template>
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="max-w-md w-full space-y-8">
			<div>
				<h2
					class="mt-6 text-center text-3xl font-extrabold text-gray-900">
					Войти в аккаунт
				</h2>
			</div>
			<form
				class="mt-8 space-y-6"
				@submit.prevent="handleLogin">
				<div class="rounded-md shadow-sm -space-y-px">
					<div class="mb-5">
						<input
							v-model="email"
							type="email"
							required
							class="input-field rounded-t-md"
							placeholder="Адрес электронной почты" />
					</div>
					<div>
						<input
							v-model="password"
							type="password"
							required
							class="input-field rounded-b-md"
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
						Войти
					</button>
				</div>

				<div class="text-center">
					<router-link
						to="/register"
						class="text-blue-600 hover:text-blue-500">
						Нет аккаунта? Зарегистрироваться
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
	const email = ref("");
	const password = ref("");
	const error = ref("");

	const handleLogin = async () => {
		const result = await authStore.login({
			email: email.value,
			password: password.value,
		});
        console.log(result)

		if (result.success) {
			router.push("/dashboard");
		} else {
			error.value = result.error;
		}
	};
</script>
