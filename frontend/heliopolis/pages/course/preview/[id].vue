<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const course_details = ref();

async function retrive_course_data() {
  const token = localStorage.getItem("token");
  await axios
    .get(
      `http://127.0.0.1:8000/api/v1/course-details-after-enrollment/?course_id=${parseInt(
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
      console.log(err.response.status);
      if (err.response.status === 403 || err.response.status === 401) {
        router.push({ path: "/" });
      }
    });
}

const selected_index = ref();
const open = ref(false);

const lesson_obj = ref();
const lesson_section_open = ref(false);

const show_review = ref();

function expand_chapter(index) {
  selected_index.value = index;
  open.value = !open.value;
}

function lesson(obj) {
  lesson_obj.value = obj;
  lesson_section_open.value = true;
}

async function open_review() {
  show_review.value = !show_review.value;
  await retrive_review();
}

const rating = ref();
const review = ref();

const error = ref();

async function submit_review() {
  const token = localStorage.getItem("token");

  const data = {
    rating: rating.value,
    review: review.value,
  };

  console.log(data);
  await axios
    .post(
      `http://127.0.0.1:8000/api/v1/review_rating/?course_id=${route.params.id}`,
      data,
      {
        headers: {
          Authorization: token,
          "Content-Type": "multipart/form-data",
        },
      }
    )
    .then((res) => {
      console.log(res);
      review.value = ''
      rating.value = ''
      retrive_review()
    })
    .catch((err) => {
      error.value = err.response.data[0]
      console.log(err);
      console.log(error.value)
    });
}

const review_obj = ref();



async function retrive_review() {
  const token = localStorage.getItem("token");

  await axios
    .get(
      `http://127.0.0.1:8000/api/v1/review_rating/?course_id=${route.params.id}`,
      {
        headers: {
          Authorization: token,
          "Content-Type": "multipart/form-data",
        },
      }
    )
    .then((res) => {
      review_obj.value = res.data.results;
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
    });
}

onMounted(async () => {
  await retrive_course_data();
});
</script>

<template>
  <div class="flex">
    <aside
      class="w-[20rem] fixed left-0 top-0 h-screen bg-gray-200 rounded-r-lg drop-shadow-md p-10"
    >
      <h1 class="text-xl text-center font-semibold">Heliopolis</h1>

      <div v-if="course_details" class="m-6 py-4">
        <div v-for="(i, index) in course_details.chapters" :key="i.id">
          <div
            class="my-2 transform ease-in-out duration-150 hover:bg-slate-300 rounded-md p-1 border-2 border-gray-300"
            role="button"
          >
            <div class="flex justify-between" @click="expand_chapter(index)">
              <div>
                <h1>Chaper {{ index + 1 }}: {{ i.chapter_title }}</h1>
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
            <div v-if="selected_index === index && open" class="">
              <div v-for="(j, index) in i.lessons" :key="index" class="my-4">
                <div
                  class="transform ease-in-out duration-150 hover:bg-slate-200 rounded-md px-2"
                  @click="lesson(j)"
                >
                  <h1>{{ j.lesson_title }}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center items-center">
        <button
          type="submit"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
          @click="open_review"
        >
          Give a review
        </button>
      </div>
    </aside>
    <main class="flex-1 ml-[21rem] mt-10">
      <div class="mx-4" v-if="lesson_section_open">
        <h1 class="text-3xl">{{ lesson_obj.lesson_title }}</h1>
        <div class="my-4">
          <video :src="lesson_obj.lesson_video" controls></video>
        </div>
      </div>

      <div v-if="show_review">
        <div class="mb-10" v-if="review_obj">
          <h1 class="text-xl font-semibold">This course got review so far</h1>
          <div v-for="(i, index) in review_obj" :key="index" class="my-4">
            <div class="flex space-x-4 items-center">
              <div class="w-12 h-12 rounded-full bg-rose-500"></div>
              <div>
                <h1 class="text-xs text-gray-400">{{ i.student }}</h1>
                <h1>
                  {{ i.rating }} 🌟
                </h1>
              </div>
            </div>

            <p class="text-gray-600 ml-16">
              {{ i.review }}
            </p>
          </div>
        </div>
        <h1 class="font-semibold mt-20">Give a review</h1>
        <p v-if="error" class="text-rose-600 text-sm italic">* Sorry, {{ error }}</p>
        <div class="my-4">
          <div class="mb-6">
            <label
              for="small-input"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Rating</label
            >
            <input
              v-model="rating"
              type="number"
              id="small-input"
              class="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div class="mb-6">
            <label
              for="message"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Your review</label
            >
            <textarea
              v-model="review"
              id="message"
              rows="4"
              class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Write your thoughts here..."
            ></textarea>
          </div>

          <div>
            <button
              type="submit"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
              @click="submit_review"
            >
              submit
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
