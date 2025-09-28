document.addEventListener('DOMContentLoaded', () => {
    const inboxAction = document.getElementById('inboxAction');
    const checkboxes = document.querySelectorAll('.form-check-input');

    // Toggle visibility of inboxAction based on checkbox state
    function updateInboxActionVisibility() {
        const anyChecked = [...checkboxes].some(cb => cb.checked);
        inboxAction.classList.toggle('active', anyChecked);
        inboxAction.classList.toggle('inactive', !anyChecked);
    }

    // Attach listener to each checkbox
    checkboxes.forEach(cb => cb.addEventListener('change', updateInboxActionVisibility));

    // Initial state check
    updateInboxActionVisibility();

    // Toggle full-message when clicking on .mail-cnt
    document.querySelectorAll('.table .mail-cnt').forEach(mailCnt => {
        mailCnt.addEventListener('click', () => {
            const fullMessage = mailCnt.closest('td')?.querySelector('.full-message');
            if (fullMessage) {
                fullMessage.classList.toggle('expanded');
            }
        });
    });
});

// Dropdown and Tag Selection for Contacts
const contacts = [
    { name: "Chetan Johnson", avatar: "https://i.pravatar.cc/150?img=1" },
    { name: "Bob Smith", avatar: "https://i.pravatar.cc/150?img=2" },
    { name: "Charlie Lee", avatar: "https://i.pravatar.cc/150?img=3" },
    { name: "Diana Prince", avatar: "https://i.pravatar.cc/150?img=4" },
    { name: "Eva Adams", avatar: "https://i.pravatar.cc/150?img=5" },
    { name: "Frank Cooper", avatar: "https://i.pravatar.cc/150?img=6" },
    { name: "George Martin", avatar: "https://i.pravatar.cc/150?img=7" }
];

const wrapper = document.getElementById("inputTagsWrapper");
const InboxsearchInput = document.getElementById("contactSearch");
const dropdown = document.getElementById("contactDropdown");

let selectedContacts = [];

function renderTags() {
    wrapper.querySelectorAll(".tag").forEach(tag => tag.remove());

    selectedContacts.forEach((contact, index) => {
        const tag = document.createElement("div");
        tag.className = "tag px-2 py-1 d-inline-flex align-items-center gap-2 rounded-pill";
        tag.innerHTML = `
        <img src="${contact.avatar}" alt="">
        ${contact.name}
        <span class="remove-tag" data-index="${index}">&times;</span>`;
        wrapper.insertBefore(tag, InboxsearchInput);
    });
}

function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, `<span class="highlight">$1</span>`);
}

function showDropdown(query) {
    dropdown.innerHTML = "";

    const matches = contacts.filter(c =>
        c.name.toLowerCase().includes(query.toLowerCase()) &&
        !selectedContacts.some(sel => sel.name === c.name)
    );

    if (matches.length) {
        matches.forEach(contact => {
            const li = document.createElement("li");
            li.className = "dropdown-item";
            li.innerHTML = `
          <img src="${contact.avatar}" alt="${contact.name}">
          <span>${highlightMatch(contact.name, query)}</span>
        `;
            li.onclick = () => {
                selectedContacts.push(contact);
                renderTags();
                InboxsearchInput.value = "";
                hideDropdown();
                InboxsearchInput.focus();
            };
            dropdown.appendChild(li);
        });

        // Width based on widest item
        const widestItem = Math.max(...[...dropdown.children].map(li => li.offsetWidth));
        // dropdown.style.width = Math.min(widestItem + 40, 300) + "px";

        // Position dropdown under input
        const inputRect = InboxsearchInput.getBoundingClientRect();
        const wrapperRect = wrapper.getBoundingClientRect();
        dropdown.style.left = (inputRect.left - wrapperRect.left) + "px";
        dropdown.style.top = (InboxsearchInput.offsetTop + InboxsearchInput.offsetHeight) + "px";
        dropdown.style.display = "block";
    } else {
        hideDropdown();
    }
}

function hideDropdown() {
    dropdown.style.display = "none";
}

InboxsearchInput.addEventListener("input", () => {
    const query = InboxsearchInput.value.trim();
    if (query) {
        showDropdown(query);
    } else {
        hideDropdown();
    }
});

wrapper.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-tag")) {
        const index = parseInt(e.target.dataset.index);
        selectedContacts.splice(index, 1);
        renderTags();
    }
    InboxsearchInput.focus();
});

document.addEventListener("click", (e) => {
    if (!e.target.closest(".contact-search-wrapper")) {
        hideDropdown();
    }
});

function toggleClass(element) {
    element.classList.toggle("open");
}
// $(document).ready(function() {
//     $('#summernote').summernote();
// });
ClassicEditor
.create(document.querySelector('#editor'), {
    // Optional: customize toolbar or plugins
})
.then(editor => {
    // Ensure editable area grows
    editor.ui.view.editable.element.style.height = '100%';
})
.catch(error => {
    console.error(error);
});