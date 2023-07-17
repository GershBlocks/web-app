// Function to fetch the message counts and update the message-count element
function fetchMessageCounts() {
  fetch('/api/message-counts')
  .then(response => response.json())
  .then(data => {
    const unreadCountElement = document.getElementById('message-count');

    // Separate the unread count and the total count from the API response
    const unreadCount = data.unread;
    const totalCount = data.total;

    // Update the text content of the unread-count element
    unreadCountElement.textContent = `You have ${unreadCount} unread message out of ${totalCount} total.`;
  })
  .catch(error => console.error('Error:', error));
}

// Call the fetchMessageCounts function on page load
window.addEventListener('load', fetchMessageCounts);


// Function to fetch inbox emails from the API
function fetchInboxEmails() {
  fetch('/api/inbox')
    .then(response => response.json())
    .then(emails => {
      const inboxContainer = document.getElementById('inbox-container');
      inboxContainer.innerHTML = '';

      emails.forEach(email => {
        const emailElement = createEmailElement(email);
        inboxContainer.appendChild(emailElement);
      });
    })
    .catch(error => console.error('Error:', error));
}


// Function to create an email element
function createEmailElement(email) {
  const emailElement = document.createElement('div');
  emailElement.classList.add('email');
  emailElement.innerHTML = `
    <h1>${email.subject}</h1>
    <p>${email.content}</p>
  `;

  // Add an event listener to open the full message when clicked
  emailElement.addEventListener('click', () => openMessage(email.id));

  return emailElement;
}

// Function to open the full message in the message.html page
function openMessage(emailId) {
  fetch(`/api/messages/${emailId}`, { method: 'PUT' })
    .then(response => response.json())
    .then(() => {
      window.location.href = `message.html?id=${emailId}`;
    })
    .catch(error => console.error('Error:', error));
}

// Call the fetchInboxEmails function on page load
window.addEventListener('load', fetchInboxEmails);