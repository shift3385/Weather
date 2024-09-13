let currentConversationId = null;
let isConversationActive = false;
let isNewConversationAllowed = true; 
let typingInterval;
let typingvalue = 50;
let isBotTyping = false;
let isBotTypingIndicator = false;
let toggleState = 0;
const states = [
    { text: "X1", value: 50 },
    { text: "X2", value: 25 },
    { text: "X3", value: 10 }
];

$(document).ready(function() {
    $(document).keydown(function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        } else if (event.key === 'Escape' && isBotTyping) {
            stopTyping();
        }
    });

    $('#toggle-btn').on('click', function() {
        toggleState = (toggleState + 1) % states.length;
        $(this).text(states[toggleState].text);
        $(this).attr('data-value', states[toggleState].value);
        typingvalue = states[toggleState].value

        showToast('Speed changed to ' + states[toggleState].text);
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('#options-menu').length) {
            $('#options-menu').hide();
        }
    });
});

function sendMessage() {
    var message = $('#user-input').val();
    if (message.trim() === '') return;

    if (!isBotTyping) {
        var chatWindow = $('#chat-window');
        chatWindow.append('<div class="user-message">' + message + '</div>');
        $('#user-input').val('');
        chatWindow.scrollTop(chatWindow[0].scrollHeight);

        $('#user-input').prop('disabled', true);
        $('#stopWriteMessage').prop('hidden', false);
        $('#sendMessage').prop('hidden', true);

        $('#clearChatWindows').prop('disabled', true);
        $('.new-conversation-button').prop('disabled', true);
        $('.clear-history-button').prop('disabled', true);
        $('.conversation-item').addClass('disabled-item');

        var botTypingIndicator = $('<div class="bot-message typing-indicator">Thinking...</div>');
        isBotTypingIndicator = true;
        chatWindow.append(botTypingIndicator);
        chatWindow.scrollTop(chatWindow[0].scrollHeight);

        isBotTyping = true;

        $.post('/send_message', { message: message }, function (data) {
            botTypingIndicator.remove();
            isBotTypingIndicator = false;
            var botMessageContainer = $('<div class="bot-message"></div>');
            chatWindow.append(botMessageContainer);
            chatWindow.scrollTop(chatWindow[0].scrollHeight);
            const htmlText = marked.parse(markdownText);
            chatWindow.innerHTML = htmlText;

            // typeWriterEffect(botMessageContainer, data.bot_response, typingvalue, function () {
            //     stopTyping();
            // });
        });
    } else {
        stopTyping();
    }
}

function cleanText(text) {
    return text.replace(/[\*#]/g, '');
}
function addLineBreaks(text) {
    return text.replace(/([:.])/g, '$1\n');
}

function typeWriterEffect(element, text, speed, callback = null) {
    let i = 0;

    typingInterval = setInterval(function () {
        if (i < text.length) {
            element.append(text.charAt(i));
            i++;
        } else {
            clearInterval(typingInterval);
            if (callback) callback(); 
        }
    }, speed);
}

function stopTyping() {
    if( isBotTypingIndicator == false){
        clearInterval(typingInterval); 
        isBotTyping = false;
        $('#stopWriteMessage').prop('hidden', true);
        $('#sendMessage').prop('hidden', false);
        enableControls(); 
    }
}

function enableControls() {
    $('#user-input').prop('disabled', false);
    $('#clearChatWindows').prop('disabled', false);
    $('#sendMessage').html('<i class="fas fa-pencil"></i>');
    $('.new-conversation-button').prop('disabled', false);
    $('.clear-history-button').prop('disabled', false);
    $('.conversation-item').removeClass('disabled-item');
}

function newConversation() {
    if (isConversationActive) {
        saveCurrentConversation(function() {
            $('#chat-window').empty();
            $('#user-input').val('');
            isConversationActive = false;
        });
    } else {
        if ($('#chat-window').html().trim() !== '') {
            saveCurrentConversation(function() {
                $('#chat-window').empty();
                $('#user-input').val('');
                isConversationActive = false;
            });
        }
    }
}

function loadConversation(conversationId) {
    if (isConversationActive) {
        saveCurrentConversation(function() {
            $.get('/get_conversation/' + conversationId, function(data) {
                $('#chat-window').html(data.conversation_content);
                $('#user-input').val('');
                currentConversationId = conversationId;
                isConversationActive = false;
                isNewConversationAllowed = true;
            });
        });
    } else {
        $.get('/get_conversation/' + conversationId, function(data) {
            $('#chat-window').html(data.conversation_content);
            $('#user-input').val('');
            currentConversationId = conversationId;
            isNewConversationAllowed = true;
        });
    }
}

function saveCurrentConversation(callback) {
    var chatWindowContent = $('#chat-window').html();
    
    if (chatWindowContent.trim() !== '') {
        $.post('/save_conversation', {conversation: chatWindowContent}, function(data) {
            $('#conversation-history').append('<div class="conversation-item" onclick="loadConversation(\'' + data.conversation_id + '\')">Chat ' + ($('#conversation-history .conversation-item').length + 1) + ' <i class="fas fa-ellipsis-h" onclick="showOptionsMenu(event, \'' + data.conversation_id + '\')"></i></div>');
            if (callback) callback();
        });
    } else if (callback) {
        callback();
    }
}

function showOptionsMenu(event, conversationId) {
    event.stopPropagation();
    var menu = $('#options-menu');
    menu.css({
        top: event.pageY + 'px',
        left: event.pageX + 'px'
    }).show();
    menu.data('conversationId', conversationId);
}

function deleteConversation() {
    var conversationId = $('#options-menu').data('conversationId');
    $.post('/delete_conversation', {conversation_id: conversationId}, function() {
        $('#conversation-history').find('.conversation-item').each(function() {
            if ($(this).find('i').attr('onclick').includes(conversationId)) {
                $(this).remove();
            }
        });
        $('#options-menu').hide();
    });
}

function renameConversation() {
    showRenameModal('Enter the new name for the conversation:', function(newName) {
        if (newName) {
            $('#chat-title').text(newName);
            var conversationId = $('#options-menu').data('conversationId');
            $('#conversation-history').find('.conversation-item').each(function() {
                if ($(this).find('i').attr('onclick').includes(conversationId)) {
                    $(this).html(newName + ' <i class="fas fa-ellipsis-h" onclick="showOptionsMenu(event, \'' + conversationId + '\')"></i>');
                }
            });
        }
    });
}

function showRenameModal(message, callback) {
    $('#options-menu').hide();
    $('#confirm-message').html(`${message} <input type="text" id="new-conversation-name" placeholder="New name">`);
    $('#confirm-modal').show();

    $('#confirm-yes').off('click').on('click', function() {
        const newName = $('#new-conversation-name').val();
        callback(newName);
        $('#confirm-modal').hide();
    });

    $('#confirm-no').off('click').on('click', function() {
        callback(null);
        $('#confirm-modal').hide();
    });
}

function showConfirmModal(message, callback) {
    $('#confirm-message').text(message);
    $('#confirm-modal').show();

    $('#confirm-yes').off('click').on('click', function() {
        callback(true);
        $('#confirm-modal').hide();
    });

    $('#confirm-no').off('click').on('click', function() {
        callback(false);
        $('#confirm-modal').hide();
    });
}

function clearHistory() {
    showConfirmModal('Are you sure you want to delete the entire history?', function(confirm) {
        if (confirm) {
            $('#conversation-history').empty();
            $.post('/clear_history')
            
        }
    });
}

function clearChat() {
    showConfirmModal('Are you sure you want to delete the entire chat?', function(confirm) {
        if (confirm) {
            $('#chat-window').empty();
        }
    });
}

function toggleAside() {
    const aside = document.querySelector('.aside');
    aside.classList.toggle('expanded');
    
    const toggle_icon = document.querySelector('i#toggle-icon');
    if (aside.classList.contains('expanded')) {
        toggle_icon.classList.remove('fa-angle-double-right');
        toggle_icon.classList.add('fa-angle-double-left');
    } else {
        toggle_icon.classList.remove('fa-angle-double-left');
        toggle_icon.classList.add('fa-angle-double-right');
    }
}

function showToast(message) {
    var toast = document.getElementById('toast-notification');
    toast.innerText = message;

    toast.classList.remove('toast_hidde');
    toast.classList.add('toast_show');

    setTimeout(function() {
        toast.classList.remove('toast_show');
        toast.classList.add('toast_hidde');
    }, 2000); 
}