function toggle_view() {
  // Select all view more buttons
  let viewMoreBtns = document.querySelectorAll(".view_more");

  // Loop through each view more button
  viewMoreBtns.forEach(viewMoreBtn => {
      // Add click event listener to each button
      viewMoreBtn.addEventListener("click", function() {
          // Find the closest specs section relative to the clicked button
          let specs = this.closest(".product").querySelector(".specs");

          // Toggle the visibility of the specs section
          if (specs.style.display === "block") {
              specs.style.display = "none";
              this.querySelector('.text_change').textContent = "View More Specs";
              this.querySelector('.entity').style.transform = "rotate(0deg)";
          } else {
              specs.style.display = "block";
              this.querySelector('.text_change').textContent = "View Less Specs";
              this.querySelector('.entity').style.transform = "rotate(-90deg)";
          }
      });
  });
}

// Call the function to apply the toggle functionality
toggle_view();

function setupLazyLoading() {
  console.log("Setting up lazy loading...");

  const divSelector = ".lazy-div";
  const imgSelector = "img[data-src]";
  const contentSelector = ".lazy-content";

  // Callback function for the Intersection Observer
  const callback = (entries) => {
    entries.forEach((entry) => {
      // Check if the observed element is intersecting the root (viewport)
      if (entry.isIntersecting) {
        const div = entry.target;  // The element being observed
        const images = div.querySelectorAll(imgSelector);  // Select all images within this div
        const content = div.querySelectorAll(contentSelector);  // Select all lazy content within this div

        // Lazy load images by setting their src attributes
        images.forEach((img) => {
          const src = img.getAttribute("data-src");
          if (src) {
            img.setAttribute("src", src);
          }
        });

        // Remove the lazy-content class to reveal the content
        content.forEach((c) => {
          console.log("enter to remove");
          c.classList.remove(contentSelector.replace(".", ""));  // Remove the leading dot
          console.log("class removed");
        });
      }
    });
  };

  // Set up the options object for the Intersection Observer
  const options = {
    root: null,  // Use the viewport as the root
    rootMargin: "0px",  // No margin around the root
    threshold: 0.1,  // Trigger the callback when 10% of the element is visible
  };

  // Create a new Intersection Observer instance with the callback function
  const observer = new IntersectionObserver(callback, options);

  // Select the div elements you want to lazy load
  const lazyDivs = document.querySelectorAll(divSelector);
  console.log(`Found ${lazyDivs.length} elements with selector ${divSelector}`);

  // Observe each lazy div element
  lazyDivs.forEach((div) => {
    console.log("for each is running");
    observer.observe(div);  // Start observing this div
  });
}

// Usage example:
setupLazyLoading();




// This is the filter buttons events
document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById("toggleButton");
  const accDiv = document.querySelector(".acc-div");
  console.log(accDiv);

  toggleButton.addEventListener("click", function () {
    console.log("event");
    if (accDiv.style.display === "none") {
      accDiv.style.display = "block";
    } else {
      accDiv.style.display = "none";
    }
  });
});

let second_div = document.getElementsByClassName("additional-checkbox");

function change_Mainimg() {
  let productCards = document.querySelectorAll(".product-images");
  console.log(productCards);

  productCards.forEach((productCard) => {
    let changeBtns = productCard.querySelectorAll(".change-img");
    console.log(changeBtns);

    let mainImg = productCard.querySelector(".img-fluid");
    console.log(mainImg);

    changeBtns.forEach((changeBtn) => {
      changeBtn.addEventListener("click", function () {
        mainImg.src = changeBtn.src;
      });
    });
  });
}
change_Mainimg();


function toggleCustomActiveClass() {
  // Select all images with class "small"
  const images = document.querySelectorAll(".small");

  // Loop through each image
  images.forEach((image) => {
    // Add click event listener to each image
    image.addEventListener("click", () => {
      // Find the parent product container of the clicked image
      const productContainer = image.closest(".product");

      // Toggle the class only within the specific product container
      if (!image.classList.contains("custom-active")) {
        // Remove "custom-active" class from all images within the product container
        productContainer.querySelectorAll(".small").forEach((otherImage) => {
          otherImage.classList.remove("custom-active");
          otherImage.classList.add("custom-hover");
        });

        // Add "custom-active" class to the clicked image
        image.classList.add("custom-active");
      } else {
        // If the clicked image already has "custom-active" class, remove it
        image.classList.remove("custom-active");
      }
    });
  });
}

// Call the function to enable the toggle functionality
toggleCustomActiveClass();




const productContainer = document.getElementById("product-container");
console.log(`this is product container ${productContainer}`)



// function for updating cards after filtering or performing ajax request
function UpdateProductCards(products) {
  console.log("enter in the function");
  const productContainer = document.getElementById("product-container");
  console.log(`this is product container ${productContainer}`)
  productContainer.innerHTML = ""; // Clear existing product cards

  products.forEach((product) => {
    const productCardHTML = `
    <div class="mt-4 custom-rounded-top" style="background-color: #F5F6F7;">
                <div class="row">

                    <!-- Product Image section starts from here -->
                    <div class="col-md-4 d-flex p-2 product-images">
                    <div class="order-2">
                        <img src="{{product.main_img.url}}" alt="" id="main-img" class="img-fluid mt-5">
                        <div class="mt-3 text-center">
                                <div class="circle circle-active" id="circle1"></div>
                                <div class="circle" id="circle2"></div>

                        </div>
                    </div>


                    <div class="order-1 p-3">
                        <br>
                        <div class="p-1 mt-3 custom-active" style="height: 35px;"><img src="{{product.main_img.url}}"
                                    class="change-img" id="small-img" alt="" height="25px" width="30px"></div>
                            <br>
                            <div class="img-list custom-active border" style="height: 35px;">
                                {% for product_image in product.p_image.all|slice:":1" %}
                                <img src="{{product_image.image.url}}" class="change-img" alt="dd" height="25px"
                                    width="30px">
                                {% endfor %}

                            </div>
                    </div>
                </div>

                    <!-- Products Detail Section -->
                    <div class="col-md-8 py-4">
                        <div class="row my_row">
                                <div class="col-lg-4 col-md-12 col-sm-12">
                                    <h3 class="text-nowrap ms-2 " id="product-title"><a href="detail_product/{{product.id}}" id="product-link">{{ product.name }}</a></h3>
                                    <span id="product-model" class="ms-2">Model: {{product.model}}</span>
                                </div>
                                <div class="col-lg-8 col-md-12 col-sm-12 price-div">
                                    <div class="card_price_text">
                                        <span class="">Starting at</span>
                                        <span id="product-price">{{product.price}}</span>
                                    </div>
                                    <div class="below-price mt-1">
                                        <span class="p-2">Financing Offers</span>
                                        <span class="p-1 L-m L-m-n">Learn More</span>
                                        <span class="L-m-n">Pre-Qualify</span>

                                    </div>
                                </div>
                        </div>

                        <!-- Key Features -->
                        <div class="">
                            <h5 class="ms-2">Key Features:</h5>
                            <div class="row m-1 bg-white p-3">

                                <div class="col-xl-4 text-center-xl border-xl-start-primary">
                                    <span class="custom-font">New, portable and powerful PC with built-in AI</span>
                                </div>
                                <div class="col-xl-4 text-center-xl key-features">
                                    <span class="custom-font">Up to 3.2k+ OLED display</span>
                                </div>
                                <div class="col-xl-4 text-center-xl key-features">
                                    <span class="custom-font">Up to 21 hours of battery life with FHD+</span>
                                </div>
                            </div>
                        </div>

                        <!-- Customizable Specs -->
                        <div>
                            <h5 class="ms-2">Customizable Specs:</h5>
                            <div class="row">
                                <div class="col-xl-7">
                                    <div class="for_text_align">
                                        <span class="custom-font mt-1 ms-2">Processor</span>
                                        <div class="text-nowrap spec-detail ms-2"
                                            id="product-processor">
                                            <span class="ms-2">{{product.short_processor_details}}</span>
                                        </div>
                                    </div>
                                    <div class="for_text_align">
                                        <div class="custom-font mt-1 ms-2">OS</div>
                                        <div class="text-nowrap spec-detail ms-2" id="product-os">
                                            <span class="ms-2">{{product.os}}</span>
                                        </div>
                                    </div>
                                    <div class="for_text_align">
                                        <div class="custom-font mt-1 ms-2">Graphics</div>
                                        <div class="spec-detail ms-2"
                                            id="product-graphics">
                                            <span class="ms-2 text-center">{{product.graphics}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-xl-4">
                                    <div class="specs">
                                        <div class="for_text_align">
                                            <div class="custom-font mt-1 ms-2">Memory(RAM)
                                            </div>
                                            <div class="spec-detail ms-2" id="product-memory">Up to
                                                {{product.memory}}</div>
                                        </div>
                                        <div class="for_text_align">
                                            <div class="custom-font mt-1 ms-2">
                                                Storage</div>
                                            <div class="text-nowrap spec-detail ms-2"
                                                id="product-storage">Up 512 GB </div>
                                        </div>
                                        <div class="for_text_align">
                                            <div class="custom-font mt-1 ms-2">Display</div>
                                            <div class="text-nowrap spec-detail ms-2" id="product-display">
                                                {{product.display}}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="view_more ms-2 mt-2" id="view">
                                <p id="text_change">View More Specs</p>
                                <i class="bi bi-chevron-right" id="entity"></i>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
            
        `;

    productContainer.innerHTML += productCardHTML;
    const newProductCard = productContainer.lastElementChild;
    newProductCard.querySelector("#product-link").textContent = product.name;
    newProductCard.querySelector(
      "#product-model"
    ).textContent = `Model : ${product.model}`;
    newProductCard.querySelector(
      "#product-price"
    ).textContent = `$${product.price}`;
    newProductCard.querySelector("#product-processor").textContent =
      product.short_processor_details;
    newProductCard.querySelector("#product-os").textContent = product.os;
    newProductCard.querySelector("#product-graphics").textContent =
      product.graphics;
    newProductCard.querySelector("#product-memory").textContent =
      product.memory;
    newProductCard.querySelector("#product-display").textContent =
      product.display;

    let img = newProductCard.querySelector("#main-img");
    img.src = product.img;

    let small_img = newProductCard.querySelector("#small-img");
    small_img.src = product.img;

    let imgListDiv = newProductCard.querySelector(".img-list");
    console.log(`this is image list div ${imgListDiv}`);

    // Clear existing content
    imgListDiv.innerHTML = "";

    if (product.image_urls && product.image_urls.length > 0) {
      for (let i = 0; i < 1; i++) {
        let img = document.createElement("img");
        img.src = product.image_urls[i];
        img.alt = "Image";
        img.height = "20";
        img.width = "30";
        img.classList.add("change-img");
        imgListDiv.appendChild(img);
      }
    }

    // newProductCard.querySelector('#main-img').style.src = product.img;
    // Set other product details similarly
  });
}

function applyFilters() {
  let checkedCheckboxes = document.querySelectorAll(
    'input[type="checkbox"]:checked'
  );
  console.log(`this is checked checkboxes ${checkedCheckboxes}`);

  const filters = [];
  checkedCheckboxes.forEach((checkbox) => {
    filters.push(
      `${checkbox.getAttribute("data-field")}=${encodeURIComponent(
        checkbox.value
      )}`
    );
  });

  console.log(`filter list ${filters}`);

  const queryString = filters.join("&");

  fetch(`/filter_data?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      UpdateProductCards(data.data);
      setupLazyLoading()
      toggle_view();
      attachEventListeners();
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  console.log(`this is checkboxes ${checkboxes}`);
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      applyFilters();
    });
  });
});

document.getElementById("circle1").addEventListener("click", function () {
  console.log("circle clicked");
  this.classList.toggle("selected");
  document.getElementById("circle2").classList.remove("selected");
});

document.getElementById("circle2").addEventListener("click", function () {
  console.log("circle 2 clicked");
  console.log();
  this.classList.toggle("selected");
  document.getElementById("circle1").classList.remove("selected");
});


