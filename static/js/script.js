console.log("JS Loaded");

async function loadTasks(){
    const response = await fetch('/api/tasks/');
    const tasks = await response.json();

    console.log(tasks);
}

loadTasks();