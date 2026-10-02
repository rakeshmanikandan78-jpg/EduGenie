async function generateContent() {

    const courseTitle =
        document.getElementById("courseTitle").value.trim();

    const result =
        document.getElementById("result");

    const error =
        document.getElementById("error");

    const loading =
        document.getElementById("loading");

    result.innerHTML = "";
    error.innerHTML = "";

    if (!courseTitle) {
        error.innerHTML = "Please enter a course title.";
        return;
    }

    loading.style.display = "block";

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                course_title: courseTitle
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        result.textContent = data.content;

    } catch (error) {

        document.getElementById("error").textContent =
            error.message;

    } finally {

        loading.style.display = "none";
    }
}
