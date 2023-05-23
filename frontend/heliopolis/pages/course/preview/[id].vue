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

const selected_index = ref()
const open = ref(false)

const lesson_obj = ref()
const lesson_section_open = ref(false)

function expand_chapter(index){
  selected_index.value = index
  open.value = !open.value
}

function lesson(obj){
  lesson_obj.value = obj
  lesson_section_open.value = true

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
              <div v-for="(j,index) in i.lessons" :key="index" class="my-4">
                <div class="transform ease-in-out duration-150 hover:bg-slate-200 rounded-md px-2" @click="lesson(j)">
                  <h1>{{ j.lesson_title }}</h1>
                </div>

              </div>

            </div>
          </div>
        </div>
      </div>
    </aside>
    <main class="flex-1 ml-[21rem] mt-10">

      <div class="mx-4" v-if="lesson_section_open">
        <h1 class="text-3xl">{{ lesson_obj.lesson_title }}</h1>
        <div class="my-4">
          <video :src="lesson_obj.lesson_video" controls></video>
        </div>
      </div>
    </main>
  </div>
</template>
