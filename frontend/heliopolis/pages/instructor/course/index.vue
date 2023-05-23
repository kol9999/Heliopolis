<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const course = ref();
const selected_index = ref()
const publish = ref(false);
const router = useRouter();

async function retrive_course_data() {
  const token = localStorage.getItem("token");

  await axios
    .get("http://127.0.0.1:8000/api/v1/course/", {
      headers: {
        Authorization: token,
      },
    })
    .then((res) => {
      course.value = res.data;
    })
    .catch((err) => {
      console.log(err);
     
    });
}

async function publish_change(course_id, present_State) {

  // console.log(publish.value)
  const token = localStorage.getItem("token");
  const data = {
    active: !present_State,
  };
  await axios
    .patch(`http://127.0.0.1:8000/api/v1/course/${course_id}/`, data, {
      headers: {
        Authorization: token,
      },
    })
    .then((res) => {
      retrive_course_data()
      console.log(res);
      
    })
    .catch((err) => {
      console.log(err);
    });
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
      <div class="m-20">
        <div class="flex justify-between">
          <div>
            <h1 class="text-lg font-medium">Course List</h1>
          </div>
          <div>
            <NuxtLink to="/instructor/course/upload">
              <button
                class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              >
                Upload Course
              </button>
            </NuxtLink>
          </div>
        </div>

        <div class="my-10" v-if="course">
          <div
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
          >
            <div
              v-for="(i, index) in course.results"
              :key="index"
              class="max-w-sm bg-white border border-gray-200 rounded-lg shadow 0"
            >
              <a href="#">
                <img class="rounded-t-lg" src="" alt="" />
              </a>
              <div class="p-5">
                <div class="flex justify-between">
                  <div>
                    <a href="#">
                      <h5
                        class="mb-2 text-medium font-semibold tracking-tight text-gray-900"
                      >
                        {{ i.title }}
                      </h5>
                    </a>
                  </div>

                  <div>
                    <label
                      class="relative inline-flex items-center mr-5 cursor-pointer"
                    >
                      <input
                        v-if="i.active === true "
                        type="checkbox"
                        class="sr-only peer"
                        @change="publish_change(i.id, i.active)"
                        checked
                      />
                      <input
                        v-else
                        type="checkbox"
                        class="sr-only peer"
                        @change="publish_change(i.id, i.acive)"
                      />
                      <div
                        class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                      ></div>
                      <span class="ml-1 text-sm font-sm text-gray-500"
                        >Publish</span
                      >
                    </label>
                  </div>
                </div>

                <p class="mb-3 font-normal text-gray-700">
                  Here are the biggest enterprise technology acquisitions of
                  2021 so far, in reverse chronological order.
                </p>
                <NuxtLink :to="`/instructor/course/${i.id}/`">
                  <span
                    class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
                  >
                    Preview
                    <svg
                      aria-hidden="true"
                      class="w-4 h-4 ml-2 -mr-1"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                  </span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
