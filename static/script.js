const form = document.querySelector("#profile-form");
const submitButton = document.querySelector("#submit-button");
const formMessage = document.querySelector("#form-message");
const profileCard = document.querySelector("#profile-card");
const placeholder = document.querySelector("#placeholder");
const defaultAvatar = "/static/avatar.svg";

const fields = ["name", "role", "bio", "image_url", "skills"];

function clearErrors() {
  for (const field of fields) {
    document.querySelector(`#${field}-error`).textContent = "";
    document.querySelector(`#${field}`).removeAttribute("aria-invalid");
  }
  formMessage.textContent = "";
  formMessage.classList.remove("visible");
}

function showFieldErrors(errors) {
  let hasFieldError = false;
  for (const [field, message] of Object.entries(errors)) {
    const errorElement = document.querySelector(`#${field}-error`);
    const input = document.querySelector(`#${field}`);
    if (!errorElement || !input) continue;
    errorElement.textContent = message;
    input.setAttribute("aria-invalid", "true");
    hasFieldError = true;
  }
  if (!hasFieldError) {
    formMessage.textContent = "Please check your details and try again.";
    formMessage.classList.add("visible");
  }
}

function renderProfile(profile) {
  const image = document.querySelector("#profile-image");
  image.onerror = () => {
    image.onerror = null;
    image.src = defaultAvatar;
  };
  image.src = profile.image_url || defaultAvatar;
  image.alt = profile.image_url
    ? `Profile photo of ${profile.name}`
    : "Default profile avatar";
  document.querySelector("#profile-name").textContent = profile.name;
  document.querySelector("#profile-bio").textContent = profile.bio;

  const role = document.querySelector("#profile-role");
  role.textContent = profile.role;
  role.hidden = !profile.role;

  const skillSection = document.querySelector("#skills-section");
  const skillList = document.querySelector("#skill-list");
  skillList.replaceChildren();
  for (const skill of profile.skills) {
    const tag = document.createElement("li");
    tag.className = "skill-tag";
    tag.textContent = skill;
    skillList.append(tag);
  }
  skillSection.hidden = profile.skills.length === 0;

  placeholder.hidden = true;
  profileCard.hidden = false;
}

form.addEventListener("input", (event) => {
  const errorElement = document.querySelector(`#${event.target.name}-error`);
  if (errorElement) errorElement.textContent = "";
  event.target.removeAttribute("aria-invalid");
  formMessage.textContent = "";
  formMessage.classList.remove("visible");
});

document.querySelector("#bio").addEventListener("input", (event) => {
  document.querySelector("#bio-count").textContent =
    `${event.target.value.length} / 300`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearErrors();

  const formData = new FormData(form);
  const payload = Object.fromEntries(
    ["name", "bio", "image_url", "role", "skills"].map((key) => [
      key,
      formData.get(key),
    ]),
  );

  submitButton.disabled = true;
  submitButton.classList.add("loading");
  submitButton.setAttribute("aria-busy", "true");

  try {
    const response = await fetch("/generate-profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) {
      if (result.fields) showFieldErrors(result.fields);
      else {
        formMessage.textContent = result.error || "Unable to generate your profile.";
        formMessage.classList.add("visible");
      }
      return;
    }
    renderProfile(result.profile);
  } catch {
    formMessage.textContent = "Could not reach the server. Please try again.";
    formMessage.classList.add("visible");
  } finally {
    submitButton.disabled = false;
    submitButton.classList.remove("loading");
    submitButton.removeAttribute("aria-busy");
  }
});
