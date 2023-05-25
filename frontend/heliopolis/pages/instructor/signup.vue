
<script setup>
import axios from "axios";

import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';

// reactive state
const state = ref(1);
const email = ref();
const password = ref();
const loading = ref(false);
const msg = ref("");
const show_msg = ref(false);
const otp = ref()

const email_error = ref('')


const router = useRouter();

// functions that mutate state and trigger updates
// function increment() {
//   count.value++
// }

function showSignIn() {
  state.value = 1;
}

function showSignUp() {
  state.value = 2;
}

function showOtp(){
    state.value = 3
}

function show_bottom_msg(value) {
  msg.value = value;
  show_msg.value = true;
  setTimeout(() => {
    msg.value = "";
    show_msg.value = false;
  }, 3000);
}

async function signUp() {
  loading.value = true;
  const data = {
    email: email.value,
    password: password.value,
  };
  await axios
    .post("http://127.0.0.1:8000/api/v1/register-instructor/", data)
    .then((res) => {
      console.log(res);
      loading.value = false;
      show_bottom_msg("Successfully account created");
      showOtp()
    })
    .catch((err) => {
    //   console.log(err.response.data.message.email[0]);
      email_error.value = err.response.data.message.email[0]
      loading.value = false;
    });
}

async function submit_otp(){
    loading.value = true
    const data = {
        email: email.value,
        otp: otp.value
    }
    await axios.post("http://127.0.0.1:8000/api/v1/token-validation/", data)
    .then(res => {
        loading.value = false;
        show_bottom_msg("account verified");
        localStorage.setItem('token', `Token ${res.data.message.token}`);
        router.push({ path: '/instructor/course/' })
    })
    .catch((err) => {
        loading.value = false;
        console.log(err)
    })
}

// // lifecycle hooks
// onMounted(() => {
//   console.log(`The initial count is ${count.value}.`)
// })
</script>



<template>
  <div class="grid h-screen place-items-center relative">
    <div
    v-if="state === 1"
      class="my-28 w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8"
    >
      <div>
        <form class="space-y-6"  @submit.prevent="signUp">
          <h1 class="text-center text-3xl font-semibold">Heliopolis</h1>
          <h5 class=" font-medium text-gray-900 text-center">
            Sign up to our platform as an Instructor
          </h5>
          <p v-if="email_error" class="text-sm text-red-600 text-center">{{ email_error }}</p>
          <div>
            <label
              for="email"
              class="block mb-2 text-sm font-medium text-gray-900"
              >Your email</label
            >
            <input
              type="email"
              name="email"
              id="email"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="name@company.com"
              required
              v-model="email"
            />
          </div>
          <div>
            <label
              for="password"
              class="block mb-2 text-sm font-medium text-gray-900"
              >Your password</label
            >
            <input
              type="password"
              name="password"
              id="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              required
              v-model="password"
            />
          </div>
          <div class="flex items-start">
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  id="remember"
                  type="checkbox"
                  value=""
                  class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300"
                  
                />
              </div>
              <label
                for="remember"
                class="ml-2 text-sm font-medium text-gray-900"
                >Remember me</label
              >
            </div>
            <a href="#" class="ml-auto text-sm text-blue-700 hover:underline"
              >Lost Password?</a
            >
          </div>
          <button
            v-if="!loading"
            type="submit"
            class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            Create Account
          </button>

          <button
            v-if="loading"
            type="submit"
            class="w-full text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
            disabled
          >
            loading...
          </button>


          <div class="text-sm font-medium text-gray-500">
            Already have an account?
            <NuxtLink to="/">
                <span
              
              class="text-blue-700 hover:underline"
              role="button"
              >Login</span
            >
            </NuxtLink>
            
          </div>
        </form>
      </div>
    </div>


    <div>
        <div
      v-if="state == 3"
      class="my-28 w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8"
    >
      <div>
        <form class="space-y-6" @submit.prevent="submit_otp">
          <h1 class="text-center text-3xl font-semibold">Heliopolis</h1>
          <h5 class="text-xl font-medium text-gray-900 text-center">
            Verify your accout
          </h5>

          <div>
            <label
              for="email"
              class="block mb-2 text-sm font-medium text-gray-900"
              >Otp</label
            >
            <input
              type="text"
              name="email"
              id="email"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="1234"
              required
              v-model="otp"
            />
          </div>
          <button
            v-if="!loading"
            type="submit"
            class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            Verify
          </button>

          <button
            v-if="loading"
            type="submit"
            class="w-full text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
            disabled
          >
            loading...
          </button>

        </form>
      </div>
    </div>
    </div>

    <div v-if="show_msg" class="absolute bottom-4 left-4 bg-black rounded-lg">
      <h1 class="text-white m-1.5">{{ msg }}</h1>
    </div>


  </div>
</template>
