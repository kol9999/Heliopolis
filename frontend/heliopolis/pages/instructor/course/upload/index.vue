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
          <form>
            <div class="mb-6">
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Title</label
              >
              <input
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
                id="message"
                rows="4"
                class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 "
                
              ></textarea>
            </div>

            <button
              type="submit"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>
