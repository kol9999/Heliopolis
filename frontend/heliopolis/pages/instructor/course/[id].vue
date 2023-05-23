<script setup>
import axios from "axios";

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const route = useRoute();

// reactive state
const title = ref("");
const description = ref("");

const loading = ref(false);

const selected_index = ref();
const expand = ref(false);
const course_details = ref();

const inside_tab = ref(false);

const showModal = ref(false);
const showModalLesson = ref(false);

const showModalQuiz = ref(false);

const video = ref();
const seleted_chapter_id = ref();

const videoUrl = ref();

const showModalQuestion = ref(false);

const option_a = ref({
  value: 1,
  state: false,
});
const option_b = ref({
  value: 2,
  state: false,
});
const option_c = ref({
  value: 3,
  state: false,
});
const option_d = ref({
  value: 4,
  state: false,
});

const router = useRouter();


function expand_btn(index, id) {
  selected_index.value = index;
  expand.value = !expand.value;
  seleted_chapter_id.value = id;
}

async function retrive_course_data() {
  const token = localStorage.getItem("token");
  await axios
    .get(
      `http://127.0.0.1:8000/api/v1/course_details/?course_id=${parseInt(
        route.params.id
      )}`,
      {
        headers: {
          Authorization: token,
        },
      }
    )
    .then((res) => {
      course_details.value = res.data;
    })
    .catch((err) => {
      console.log(err);
      router.push({path:'/'})
    });
}
function toggleModal() {
  showModal.value = !showModal.value;
}

function toggleModalLesson() {
  showModalLesson.value = !showModalLesson.value;
  expand.value = true;
}

function toggleModalQuiz() {
  showModalQuiz.value = !showModalQuiz.value;
  expand.value = true;
}

function toggleModalQuestion() {
  console.log("call");
  showModalQuestion.value = !showModalQuestion.value;
  expand.value = true;
}

async function upload_chapter() {
  loading.value = true;
  const token = localStorage.getItem("token");
  const data = {
    course: parseInt(route.params.id),
    title: title.value,
    description: description.value,
  };

  console.log(data);

  await axios
    .post("http://127.0.0.1:8000/api/v1/chapter/", data, {
      headers: {
        Authorization: token,
      },
    })
    .then((res) => {
      loading.value = false;
      console.log(res.data);
      title.value = "";
      description.value = "";
      retrive_course_data();
      toggleModal();
      // router.push({path:`/instructor/course/${id}/`})
    })
    .catch((err) => {
      loading.value = false;
      // title_error.value = err.response.data.title[0];
      console.log(err);
    });
}

async function upload_lesson() {
  loading.value = true;
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append("chapter", seleted_chapter_id.value);
  formData.append("title", title.value);
  formData.append("video", video.value);
  formData.append("type", 1);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/v1/lesson/",
      formData,
      {
        headers: {
          Authorization: token,
          "Content-Type": "multipart/form-data",
        },
      }
    );

    loading.value = false;
    console.log(response.data);
    title.value = "";
    video.value = "";
    retrive_course_data();
    expand.value = true;
    toggleModalLesson();
    // router.push({path:`/instructor/course/${id}/`})
  } catch (error) {
    loading.value = false;
    console.log(error);
  }
}

// upload quiz
async function upload_quiz() {
  loading.value = true;
  const token = localStorage.getItem("token");
  const formData = new FormData();
  const data = {
    chapter: seleted_chapter_id.value,
    title: title.value,
    type: 2,
  };
  // formData.append("chapter", seleted_chapter_id.value);
  // formData.append("title", title.value);
  // formData.append("video", video.value);
  // formData.append("type", 1);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/v1/lesson/",
      data,
      {
        headers: {
          Authorization: token,
          "Content-Type": "multipart/form-data",
        },
      }
    );

    loading.value = false;
    console.log(response.data);
    title.value = "";
    retrive_course_data();
    expand.value = true;
    toggleModalQuiz();
    // router.push({path:`/instructor/course/${id}/`})
  } catch (error) {
    loading.value = false;
    console.log(error);
  }
}
// upload quiz

function handleFileChange(event) {
  video.value = event.target.files[0];
  const videourl = URL.createObjectURL(event.target.files[0]);
  videoUrl.value = videourl;
}

onMounted(async () => {
  retrive_course_data();
});
</script>

<template>
  <div class="flex">
    <aside
      class="w-56 fixed left-0 top-0 h-screen bg-gray-200 rounded-r-lg drop-shadow-md p-10"
    >
      <h1 class="text-xl text-center font-semibold">Heliopolis</h1>
    </aside>
    <main class="flex-1 ml-44">
      <div class="m-20" v-if="course_details">
        <!-- <p>{{ course_details }}</p> -->

        <div class="flex justify-between items-center max-w-6xl">
          <div>
            <h1 class="text-xl font-semibold">
              Course: {{ course_details.title }}
            </h1>
            <p class="text-sm text-gray-500 py-2">
              {{ course_details.description }}
            </p>
          </div>

          <div>
            <button
              @click="toggleModal"
              class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Add Chapter
            </button>
          </div>
        </div>

        <div class="my-4">
          <div
            class="bg-gray-100 drop-shadow-sm rounded-md max-w-6xl my-4 transition ease-in-out duration-150 hover:drop-shadow-md"
            v-for="(i, index) in course_details.chapters"
            role="button"
            :key="index"
          >
            <div class="p-4" @click="expand_btn(index, i.id)">
              <div class="flex justify-between items-center">
                <div>
                  <h1 class="font-semibold">
                    Chapter {{ index + 1 }}: {{ i.chapter_title }}
                  </h1>
                </div>
                <div>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19.5 8.25l-7.5 7.5-7.5-7.5"
                    />
                  </svg>
                </div>
              </div>

              <div class="" v-if="index === selected_index && expand">
                <div
                  class="my-4 mx-4"
                  v-for="(j, index) in i.lessons"
                  :key="index"
                >
                  <div
                    class="flex items-center space-x-2 transform ease-in-out duration-150 hover:bg-gray-200 py-1.5 hover:rounded-md"
                  >
                    <div>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        class="w-6 h-6"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184"
                        />
                      </svg>
                    </div>
                    <div class="flex space-x-2 items-center">
                      <div>
                        <h1>{{ j.lesson_title }}</h1>
                      </div>
                      <div
                        v-if="j.lesson_type === 2"
                        class="text-xs italic underline text-blue-600"
                        @click.stop="toggleModalQuestion"
                      >
                        add question
                      </div>
                    </div>
                  </div>
                  <div class="mx-8" v-if="j.lesson_video">
                    <video :src="j.lesson_video" controls></video>
                  </div>
                </div>

                <div class="flex justify-end mx-4 space-x-2">
                  <div @click="toggleModalQuiz()">
                    <p class="underline text-blue-800 italic text-sm">
                      add quiz
                    </p>
                  </div>
                  <div @click="toggleModalLesson()">
                    <p class="underline text-blue-800 italic text-sm">
                      add lesson
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- chapter add  -->

      <div
        v-if="showModal"
        class="overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex"
      >
        <div class="relative w-auto my-6 mx-auto max-w-3xl">
          <!--content-->
          <div
            class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none"
          >
            <!--header-->
            <div
              class="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t"
            >
              <h3 class="text-2xl font-semibold">Add Chapter</h3>
              <button
                class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                @click="toggleModal()"
              >
                <span
                  class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none"
                >
                  ×
                </span>
              </button>
            </div>
            <!--body-->
            <div class="w-[40rem] p-6">
              <form>
                <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Title</label
                  >
                  <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
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

                <!-- <button
                  v-if="!loading"
                  type="submit"
                  class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                >
                  Submit
                </button>

                <button
                  v-if="loading"
                  type="submit"
                  class="text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
                  disabled
                >
                  loading...
                </button> -->
              </form>
            </div>
            <!--footer-->
            <div
              class="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b"
            >
              <button
                class="text-red-500 bg-transparent border border-solid border-red-500 hover:bg-red-500 hover:text-white active:bg-red-600 font-bold uppercase text-sm px-6 py-1.5 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="toggleModal()"
              >
                Close
              </button>
              <button
                v-if="!loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="upload_chapter()"
              >
                Save Changes
              </button>

              <button
                v-if="loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150 animate-pulse"
                type="button"
              >
                loading...
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showModal"
        class="opacity-25 fixed inset-0 z-40 bg-black"
      ></div>

      <!-- chapter add  -->

      <!-- lesson add  -->

      <div
        v-if="showModalLesson"
        class="overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex"
      >
        <div class="relative w-auto my-6 mx-auto max-w-3xl">
          <!--content-->
          <div
            class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none"
          >
            <!--header-->
            <div
              class="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t"
            >
              <h3 class="text-2xl font-semibold">Add lesson</h3>
              <button
                class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                @click="toggleModalLesson()"
              >
                <span
                  class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none"
                >
                  ×
                </span>
              </button>
            </div>
            <!--body-->
            <div class="w-[40rem] p-6">
              <form>
                <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Title</label
                  >
                  <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                  <input
                    v-model="title"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                    required
                  />
                </div>
                <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Video</label
                  >
                  <div
                    class="flex items-center justify-center w-full"
                    v-if="!videoUrl"
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
                          Mp4(small video for test purpose)
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
                    <video :src="videoUrl" controls></video>
                  </div>
                  <!-- <textarea
                    v-model="video"
                    id="message"
                    rows="4"
                    class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700"
                  ></textarea> -->
                </div>

                <!-- <button
                  v-if="!loading"
                  type="submit"
                  class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                >
                  Submit
                </button>

                <button
                  v-if="loading"
                  type="submit"
                  class="text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
                  disabled
                >
                  loading...
                </button> -->
              </form>
            </div>
            <!--footer-->
            <div
              class="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b"
            >
              <button
                class="text-red-500 bg-transparent border border-solid border-red-500 hover:bg-red-500 hover:text-white active:bg-red-600 font-bold uppercase text-sm px-6 py-1.5 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="toggleModalLesson()"
              >
                Close
              </button>
              <button
                v-if="!loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="upload_lesson()"
              >
                Save Changes
              </button>
              <button
                v-if="loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150 animate-pulse"
                type="button"
                v-on:click="upload_lesson()"
              >
                loading...
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showModalLesson"
        class="opacity-25 fixed inset-0 z-40 bg-black"
      ></div>
      <!-- lesson add  -->

      <!-- quiz add -->
      <div
        v-if="showModalQuiz"
        class="overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex"
      >
        <div class="relative w-auto my-6 mx-auto max-w-3xl">
          <!--content-->
          <div
            class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none"
          >
            <!--header-->
            <div
              class="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t"
            >
              <h3 class="text-2xl font-semibold">Add quiz</h3>
              <button
                class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                @click="toggleModalQuiz()"
              >
                <span
                  class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none"
                >
                  ×
                </span>
              </button>
            </div>
            <!--body-->
            <div class="w-[40rem] p-6">
              <form>
                <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Quiz title</label
                  >
                  <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                  <input
                    v-model="title"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                    required
                  />
                </div>
                <!-- <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Video</label
                  >
                  <div class="flex items-center justify-center w-full" v-if="!videoUrl">
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
                          Mp4(small video for test purpose)
                        </p>
                      </div>
                      <input id="dropzone-file" type="file" class="hidden" @change="handleFileChange"/>
                    </label>
                  </div>

                  <div v-else>
                    <video :src="videoUrl" controls></video>
                  </div>
                 
                </div> -->

                <!-- <button
                  v-if="!loading"
                  type="submit"
                  class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                >
                  Submit
                </button>

                <button
                  v-if="loading"
                  type="submit"
                  class="text-white bg-blue-300 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center animate-pulse"
                  disabled
                >
                  loading...
                </button> -->
              </form>
            </div>
            <!--footer-->
            <div
              class="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b"
            >
              <button
                class="text-red-500 bg-transparent border border-solid border-red-500 hover:bg-red-500 hover:text-white active:bg-red-600 font-bold uppercase text-sm px-6 py-1.5 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="toggleModalQuiz()"
              >
                Close
              </button>
              <button
                v-if="!loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="upload_quiz()"
              >
                Save Changes
              </button>
              <button
                v-if="loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150 animate-pulse"
                type="button"
              >
                loading...
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showModalQuiz"
        class="opacity-25 fixed inset-0 z-40 bg-black"
      ></div>
      <!-- quiz add -->

      <!-- question modal -->
      <div
        v-if="showModalQuestion"
        class="overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex"
      >
        <div class="relative w-auto my-6 mx-auto max-w-3xl">
          <!--content-->
          <div
            class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none"
          >
            <!--header-->
            <div
              class="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t"
            >
              <h3 class="text-2xl font-semibold">Add qustion</h3>
              <button
                class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                @click="toggleModalQuestion()"
              >
                <span
                  class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none"
                >
                  ×
                </span>
              </button>
            </div>
            <!--body-->
            <div class="w-[40rem] p-6">
              <form>
                <div class="mb-6">
                  <label
                    for="email"
                    class="block mb-2 text-sm font-medium text-gray-900"
                    >Quetion</label
                  >
                  <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                  <input
                    v-model="title"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                    required
                  />
                </div>

                <div class="border-[1px] border-cyan-400 p-4">
                  <div class="mb-6">
                    <div class="flex justify-between">
                      <div>
                        <label
                          for="email"
                          class="block mb-2 text-sm font-medium text-gray-900"
                          >Option A</label
                        >
                      </div>
                      <div>
                        <label
                          class="relative inline-flex items-center mr-5 cursor-pointer"
                        >
                          <input
                            type="checkbox"
                            v-model="option_a"
                            class="sr-only peer"
                            checked
                          />

                          <div
                            class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                          ></div>
                          <span class="ml-2 text-xs text-gray-500"
                            >Right ans</span
                          >
                        </label>
                      </div>
                    </div>

                    <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                    <input
                      v-model="title"
                      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                      required
                    />
                  </div>

                  <div class="mb-6">
                    <div class="flex justify-between">
                      <div>
                        <label
                          for="email"
                          class="block mb-2 text-sm font-medium text-gray-900"
                          >Option B</label
                        >
                      </div>
                      <div>
                        <label
                          class="relative inline-flex items-center mr-5 cursor-pointer"
                        >
                          <input
                            type="checkbox"
                            v-model="option_b"
                            class="sr-only peer"
                            checked
                          />
                          <div
                            class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                          ></div>
                          <span class="ml-2 text-xs text-gray-500"
                            >Right ans</span
                          >
                        </label>
                      </div>
                    </div>
                    <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                    <input
                      v-model="title"
                      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                      required
                    />
                  </div>

                  <div class="mb-6">
                    <div class="flex justify-between">
                      <div>
                        <label
                          for="email"
                          class="block mb-2 text-sm font-medium text-gray-900"
                          >Option C</label
                        >
                      </div>
                      <div>
                        <label
                          class="relative inline-flex items-center mr-5 cursor-pointer"
                        >
                          <input
                            type="checkbox"
                            v-model="option_c"
                            class="sr-only peer"
                            checked
                          />

                          <div
                            class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                          ></div>
                          <span class="ml-2 text-xs text-gray-500"
                            >Right ans</span
                          >
                        </label>
                      </div>
                    </div>
                    <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                    <input
                      v-model="title"
                      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                      required
                    />
                  </div>

                  <div class="mb-6">
                    <div class="flex justify-between">
                      <div>
                        <label
                          for="email"
                          class="block mb-2 text-sm font-medium text-gray-900"
                          >Option D</label
                        >
                      </div>
                      <div>
                        <label
                          class="relative inline-flex items-center mr-5 cursor-pointer"
                        >
                          <input
                            type="checkbox"
                            v-model="option_d"
                            class="sr-only peer"
                            checked
                          />

                          <div
                            class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                          ></div>
                          <span class="ml-2 text-xs text-gray-500"
                            >Right ans</span
                          >
                        </label>
                      </div>
                    </div>
                    <!-- <div class="my-2" v-if="title_error">
                    <p class="text-red-600 text-sm italic">{{ title_error }}</p>
                  </div> -->
                    <input
                      v-model="title"
                      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700"
                      required
                    />
                  </div>
                </div>
              </form>
            </div>
            <!--footer-->
            <div
              class="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b"
            >
              <button
                class="text-red-500 bg-transparent border border-solid border-red-500 hover:bg-red-500 hover:text-white active:bg-red-600 font-bold uppercase text-sm px-6 py-1.5 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="toggleModalQuestion()"
              >
                Close
              </button>
              <button
                v-if="!loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                v-on:click="upload_quiz()"
              >
                Save Changes
              </button>
              <button
                v-if="loading"
                class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150 animate-pulse"
                type="button"
              >
                loading...
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showModalQuestion"
        class="opacity-25 fixed inset-0 z-40 bg-black"
      ></div>
      <!-- question modal -->
    </main>
  </div>
</template>
