<script setup>
import axios from "axios";

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

// reactive state
const title = ref("");
const description = ref("");
const thumbnail = ref()

const loading = ref(false);

const title_error = ref('')
const router = useRouter();

const image_url = ref()

async function upload_course() {
  loading.value = true;
  const token = localStorage.getItem("token");
  // const data = {
  //   title: title.value,
  //   description: description.value,
  // };
  const formData = new FormData();
  formData.append("title", title.value);
  formData.append("description", description.value);
  formData.append("thumbnail", thumbnail.value);

  await axios
    .post("http://127.0.0.1:8000/api/v1/course/", formData, {
      headers: {
        Authorization: token,
      },
    })
    .then((res) => {
      loading.value = false;
      console.log(res.data);
      const id = res.data.id
      router.push({path:`/instructor/course/${id}/`})
    })
    .catch((err) => {
      loading.value = false;
      title_error.value = err.response.data.title[0]
      console.log(err);
    });
}


function handleFileChange(event) {
  thumbnail.value = event.target.files[0];
  const imageUrl = URL.createObjectURL(event.target.files[0]);
  image_url.value = imageUrl;
}

async function logout() {
  const token = localStorage.getItem("token");
  const data ={}
  await axios
    .post("http://127.0.0.1:8000/api/v1/logout/", data,{
      headers: {
        Authorization: token,
      },
    })
    .then((res) => {
      localStorage.removeItem("token");
      router.push({ path: "/" });
    });
}



// // lifecycle hooks
// onMounted(() => {
//   console.log(`The initial count is ${count.value}.`)
// })
</script>

<template>
  <div class="flex">
    <aside
      class="w-56 fixed left-0 top-0 h-screen bg-gray-200 rounded-r-lg drop-shadow-md p-10"
    >
      <div class="flex flex-col justify-between" style="height: 90vh">
        <div>
          <h1 class="text-xl text-center font-semibold">Heliopolis</h1>
        </div>
        <div @click="logout">
          <button
            class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            Logout
          </button>
        </div>
      </div>
    </aside>
    <main class="flex-1 ml-44">
      <div class="m-20">
        <div class="flex justify-between">
          <div>
            <h1 class="text-lg font-medium">Upload Course</h1>
          </div>
          <div>
            <Nuxt-Link to="/instructor">
              <button
                type="submit"
                class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              >
                Course List
              </button>
            </Nuxt-Link>
          </div>
        </div>

        <div class="my-10">
          <form @submit.prevent="upload_course">
            <div class="mb-6">
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Title</label
              >
              <div class="my-2" v-if="title_error">
                <p class="text-red-600 text-sm italic">{{ title_error }}</p>
              </div>
              <input
                v-model="title"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                required
              />
            </div>
            <div class="mb-6">
              <label
                for="message"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Description</label
              >
              <textarea
                v-model="description"
                id="message"
                rows="4"
                class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700"
              ></textarea>
            </div>


            <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Thumbnail</label
                  >
                  <div
                  v-if="!image_url"
                    class="flex items-center justify-center w-full"
                    
                  >
                    <label
                      for="dropzone-file"
                      class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
                    >
                      <div
                        class="flex flex-col items-center justify-center pt-5 pb-6"
                      >
                        <svg
                          aria-hidden="true"
                          class="w-10 h-10 mb-3 text-gray-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                          ></path>
                        </svg>
                        <p
                          class="mb-2 text-sm text-gray-500 dark:text-gray-400"
                        >
                          <span class="font-semibold">Click to upload</span> or
                          drag and drop
                        </p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">
                          Png, jpeg, jpg
                        </p>
                      </div>
                      <input
                        id="dropzone-file"
                        type="file"
                        class="hidden"
                        @change="handleFileChange"
                      />
                    </label>
                  </div>

                  <div v-else>
                    <img :src="image_url" alt="">
                  </div>

                </div>

            <button
              v-if="!loading"
              type="submit"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
            >
              Submit
            </button>

            <button
              v-if="loading"
              type="submit"
              class=" text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
              disabled
            >
              loading...
            </button>
          </form>
        </div>

        <!-- if upload done  -->
        <!-- <div v-if="uploaded">
            <div>
              <h1 class="text-xl font-semibold ">Course: {{ title_from_db }}</h1>
              <p class="text-sm text-gray-500 py-2">
                dsadsa{{ description_from_db }}
              </p>
            </div>

        </div> -->
      </div>
    </main>
  </div>
</template>
