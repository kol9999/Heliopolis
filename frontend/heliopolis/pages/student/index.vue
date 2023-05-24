<script setup>
import axios from "axios";

const course = ref();
const token = ref();

const router = useRouter();

async function retrive_course_data() {
  const token = localStorage.getItem("token");

  await axios
    .get("http://127.0.0.1:8000/api/v1/course_public_view/", {
      headers: {
        Authorization: token ? token : null,
      },
    })
    .then((res) => {
      course.value = res.data;
    })
    .catch((err) => {
      console.log(err);
      router.push({ path: "/" });
    });
}

async function enroll_now(course_id) {
  const token = localStorage.getItem("token");

  const data = {
    course: course_id,
  };
  await axios
    .post("http://127.0.0.1:8000/api/v1/enrollment/", data, {
      headers: {
        Authorization: token,
      },
    })
    .then(res => {
      retrive_course_data();
    })
    .catch((err) => {
      router.push({ path: "/" });
    });
}
function watch_now(id) {
  router.push({path:`/course/preview/${id}/`})
}

onMounted(async () => {
  retrive_course_data();
});
</script>

<template>
  <div class="max-w-7xl mx-auto">
    <main class="flex-1">
      <div class="m-20">
        <h1 class="text-3xl font-semibold">Course List</h1>

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
                <img class="rounded-t-lg" :src="i.thumbnail" alt="" />
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
                </div>

                <p class="mb-3 font-normal text-gray-700">
                  {{ i.description }}
                </p>

                <span
                  v-if="i.enroll_status"
                  class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
                >
                  <span @click="watch_now(i.id)"> Watch now </span>
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
                <!-- <NuxtLink :to="`/instructor/course/${i.id}/`"> -->
                <span
                  v-else
                  class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
                  @click="enroll_now(i.id)"
                >
                  Enroll now

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
                <!-- </NuxtLink> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
