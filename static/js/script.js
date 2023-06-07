//This const are created to allow users to subscribe to the news letter

const validateEmail = function(email) {
    var formData = new FormData();
    formData.append('email', email);
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
        url: '/validate/',
        type: 'POST',
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.error(xhr.statusText);
        },
        success: function (res) {
            $('.error').text(res.msg);
            if (res.msg){
                $('#submit').prop('disabled', true);
            }
            else {
                $('#submit').prop('disabled', false);
            }
        }
    });
};

const subscribeUser = function(email, name) {
    var formData = new FormData();
    formData.append('email', email);
    formData.append('name', name);
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
        url: '/newsletter/',
        type: 'POST',
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.error(xhr.statusText);
        },
        success: function (res) {
            $('.success').text(res.msg);
            $('#userEmail').val(' ');
            $('#userName').val(' ');
        }
    });
};

(function ($) {
    $('#submit').on('click', () => {
        event.preventDefault();
        const userEmail = $('#userEmail').val();
        const userName = $('#userName').val();
        if (userEmail && userName) {
            subscribeUser(userEmail, userName);
        }
    });

    $('#userEmail').on('change', (event) => {
        event.preventDefault();
        const email = event.target.value;
        validateEmail(email);
    });
})(jQuery);

// Get the button element
const openChatBtn = document.getElementById("open-chat-btn");

// Add click event listener to the button
openChatBtn.addEventListener("click", openChatPopup);

// Function to open the chat pop-up window
function openChatPopup() {
  // The chat pop-up window code goes here...
}

// Function to open the chat pop-up window
function openChatPopup() {
    // Create the chat pop-up window
    const chatPopup = document.createElement("div");
    chatPopup.id = "chat-popup";
    chatPopup.innerHTML = `
      <div id="chat-area">
        <div id="chat-messages">
          <p>Hello! Please select one of the following options:</p>
        </div>
        <div id="chat-buttons">
          <button id="option1">I need immediate help!</button>
          <hr>
          <button id="option2">I need to talk with someone.</button>
          <hr>
          <button id="option3">I am looking for a job.</button>
        </div>
      </div>
    `;
  
    // Add the chat pop-up window to the body element
    document.body.appendChild(chatPopup);
  
    // Add click event listeners to the buttons
    const option1Btn = document.getElementById("option1");
    const option2Btn = document.getElementById("option2");
    const option3Btn = document.getElementById("option3");
    option1Btn.addEventListener("click", option1Clicked);
    option2Btn.addEventListener("click", option2Clicked);
    option3Btn.addEventListener("click", option3Clicked);
  
    // Function to handle Option 1 click
    function option1Clicked() {
      const message = "If you are in a crisis and need urgent help, please contact your GP or Samaritans on 116 123, or dial 999.";
      addMessageToChat(message);
    }
  
    // Function to handle Option 2 click
    function option2Clicked() {
      const message = "Combat Stress provides a range of community, outpatient and residential mental health services to veterans with complex mental health problems. We provide services in-person, and via phone and online. Visit: combatstress.org.uk;  FREE HELPLINE: 0800 1381619;  Email: helpline@combatstress.org.uk"; 
      addMessageToChat(message);
    }
  
    // Function to handle Option 3 click
    function option3Clicked() {
      const message = "You can search of a job on: https://www.ex-militarycareers.com/jobs/";
      addMessageToChat(message);
    }
  
    // Function to add a message to the chat area
    function addMessageToChat(message) {
      const chatMessages = document.getElementById("chat-messages");
      const messageElement = document.createElement("p");
      messageElement.textContent = message;
      chatMessages.appendChild(messageElement);
    }
  }
  