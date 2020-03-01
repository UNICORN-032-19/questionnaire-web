var coreapi = window.coreapi;
var client = new coreapi.Client()
var currentCount = undefined;
function get_scrf_token() {
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    return csrfmiddlewaretoken;
}
function create_new_count() {
    return $.ajax({
        "async": true,
        "url" : "http://localhost:8000/api/v1/count/",
        "dataType": "json",
        "method": "POST",
        "data": {
            "csrfmiddlewaretoken" : get_scrf_token(),
            "user_id" : $( "#user" ).val(),
        },
        success : function (data) {
            currentCount = data.count_id;
            $("h3#count").html(`Count# ${currentCount}`);
        },
    });
}
function done_count() {
    var data = {
        "csrfmiddlewaretoken" : get_scrf_token(),
        "pk": parseInt(currentCount),
        "done": true,
    };
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", "http://localhost:8000/api/v1/count/" + currentCount + "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader("X-CSRFToken", get_scrf_token());
    xhr.send(JSON.stringify(data));
}
function get_questions() {
    return $.ajax({
        "async": true,
        "url" : "http://localhost:8000/api/v1/question/",
        "dataType": "json",
        "method": "GET",
        "data": {
            "csrfmiddlewaretoken" : get_scrf_token(),
            "current_count": currentCount,
        },
        success : function (data) {
            $.each(data["questions"], function(question_id) {
                var q_data = data["questions"][question_id];
                var qId = q_data.id;
                var text = q_data.text;
                var html = `
                    <h2>${text}</h2>
                    <form>
                        <input id="QID_${qId}" hidden="true" value="${qId}" multiple-answers="${q_data.multiple_answers}"/>
                `;
                var answers = q_data.answers;
                $.each(answers, function(answer_id) {
                    var answer = answers[answer_id];
                    if (q_data.multiple_answers) {
                        if (data["answered"][qId] && data["answered"][qId].includes(answer.id)){
                            html = html +
                                `<input class="answer" type="checkbox" value="${answer.id}" name="${qId}" checked>
                                    ${answer.description}
                                </input></br>
                            `;
                        } else {
                            html = html +
                                `<input class="answer" type="checkbox" value="${answer.id}" name="${qId}">
                                    ${answer.description}
                                </input></br>
                            `;
                        }
                    } else {
                        if (data["answered"][qId] && data["answered"][qId].includes(answer.id)){
                            html = html +
                                `<input class="answer" type="radio" value="${answer.id}" name="${qId}" checked>
                                    ${answer.description}
                                </input></br>
                            `;
                        } else {
                            html = html +
                                `<input class="answer" type="radio" value="${answer.id}" name="${qId}">
                                    ${answer.description}
                                </input></br>
                            `;
                        }
                    }
                });
                html = html + '</form>';
                $( "#pills-questions" ).append(html);
            });
        },
    });         
}
function get_user_answers() {
    return $.ajax({
        "async": true,
        "url" : "http://localhost:8000/api/v1/user_answer/",
        "dataType": "json",
        "method": "GET",
        "data": {
            "csrfmiddlewaretoken" : get_scrf_token(),
        },
        success : function (data) {
            $.each(data, function(question_id) {
                var html = '';
                for (username in data) {
                    html = html + `<h2>${username}</h2>`
                    for (count_id in data[username]) {
                        html = html + `<h3>Count# ${count_id}</h3>`;
                        var user_answers = data[username][count_id]["answers"];
                        var result = data[username][count_id]["result"];
                        html = html + `<h3>Result: ${result}</h3>`;
                        // for (ua in user_answers) {
                        //     var user_answer = user_answers[ua];
                        //     html = html +
                        //     '<h4>' + user_answer.text + ' : ' +
                        //     user_answer.answer + ' : ' + user_answer.is_correct +
                        //     '</h4>';
                        // }
                    }
                }
                $( "#pills-user-answers" ).append(html);
            });
        },
    });         
}

$( document ).ready(function() {
    $( ".done" ).click(function() {
        done_count();
    });
    create_new_count().done(function() {
        get_questions()
        .done(function() {
            $( ".answer" ).change(function() {
                var question = $("#QID_" + this.name);
                var answer_id = [];
                if (question.attr("multiple-answers") === "true") {
                    $("input[name='" + this.name + "']").each(function (index, element) {
                        if (element.checked) {
                            answer_id.push(parseInt(element.value));
                        }
                    })
                } else {
                    answer_id.push(parseInt(this.value));
                }
                var data = {
                    "csrfmiddlewaretoken" : get_scrf_token(),
                    "question_id": parseInt(this.name),
                    "answer_id": answer_id,
                    "count_id": parseInt(currentCount),
                };
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "http://localhost:8000/api/v1/user_answer/", true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader("X-CSRFToken", get_scrf_token());
                xhr.send(JSON.stringify(data));
            });
        });                  
    });
    get_user_answers();

});
