function fetchDepartments() {
    fetch("/departments")
      .then((response) => response.json())
      .then((data) => {
        const select = document.getElementById("select-department");
        select.innerHTML = "<option value=''>Select Department</option>";
        data.forEach((department) => {
          const option = document.createElement("option");
          option.value = department;
          option.text = department;
          select.appendChild(option);
        });
      })
      .catch((error) =>
        console.error("Error fetching departments:", error)
      );
  }

  function selectDepartment() {
    console.log("inside function");
    let selected_department =
      document.getElementById("select-department").value;
    console.log(selected_department);
    let url = "/select-department";
    fetch(url, {
      method: "post",
      body: JSON.stringify({ Department: selected_department }),
      headers: {
        "content-type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const tableBody = document
          .getElementById("facultyTable")
          .getElementsByTagName("tbody")[0];
        tableBody.innerHTML = " ";
        data.forEach((Faculty) => {
          const row = tableBody.insertRow();
          const cell1 = row.insertCell(0);
          const cell2 = row.insertCell(1);
          const cell3 = row.insertCell(2);
          const cell4 = row.insertCell(3);
          const cell5 = row.insertCell(4);

          console.log(Faculty);
          cell1.textContent = Faculty[0];
          cell2.textContent = Faculty[1];
          cell3.textContent = Faculty[2];
          cell4.textContent = Faculty[3];
          cell5.textContent = Faculty[4];
        });
        console.log(data);
      })
      .catch((err) => {
        console.log("error");
      });
  }
  fetchDepartments();