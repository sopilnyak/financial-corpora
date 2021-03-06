<template>
    <div v-if="!isLoading && result.length === 0">
        <div class="main-section">
            <input class="query" @keyup.enter="postQuery" v-model="query" ref="query" placeholder="Search..."/>
            <label class="option">
                <input type="checkbox" v-model="isExact"/>
                Exact matching
            </label>
            <div class="button option" @click="addOperator('and')">
                AND
            </div>
            <div class="button option" @click="addOperator('or')">
                OR
            </div>
            <div class="button option" @click="addOperator('not')">
                NOT
            </div>
            <label class="short">
                Max
                <input v-model="maxDocs"/>
                documents
            </label>
        </div>

        <div class="section">
            <div class="header">Filters</div>

            <div class="title">Date</div>
            <input class="date-from" type="date" v-model="dateFrom"/>
            <span class="date-middle">&rarr;</span>
            <input class="date-to" type="date" v-model="dateTo"/>
            <button class="button add" @click="addRange('date', dateFrom, dateTo)">+</button>
            <div class="example">stocks</div>
            <div class="description">documents containing 'stocks'</div>

            <div class="title">Title</div>
            <input v-model="title" @keyup.enter="addField('title', title)" class="field" placeholder="E.g. Trump"/>
            <button class="button add" @click="addField('title', title)">+</button>
            <div class="example">"stock exchange"</div>
            <div class="description">documents containing the exact phrase 'stock exchange'</div>

            <div class="title">Agency</div>
            <input v-model="agency" @keyup.enter="addField('agency', agency)" class="field" placeholder="E.g. Reuters"/>
            <button class="button add" @click="addField('agency', agency)">+</button>
            <div class="example">(Russia AND Trump) OR Arabia</div>
            <div class="description">documents containing either both 'Russia' and 'Trump' or 'Arabia'</div>

            <div class="title">Author</div>
            <input v-model="author" @keyup.enter="addField('author', author)" class="field" placeholder="E.g. Stempel"/>
            <div class="button add" @click="addField('author', author)">+</div>
            <div class="example">title:close</div>
            <div class="description">documents with titles containing 'close'</div>
        </div>

        <div class="button submit" @click="postQuery">SEARCH</div>
    </div>
    <div v-else-if="isLoading">Loading...</div>
    <div v-else>
        <div class="results-header">Search results</div>
        <div class="results-subheader">Found {{ result.n_results }} documents</div>
        <div class="results">
            <div class="results-item" v-for="document in result.results" :key="document.path">
                <div class="results-title">
                    <a :href="FlaskAddress + document.path" target="_blank">{{ document.filename }}</a>
                </div>
                <div class="results-text" v-html="document.text"></div>
            </div>
        </div>
        <div class="button submit" @click="resetResults()">NEW SEARCH</div>
    </div>
</template>

<script>
    export default {
        name: 'Search',
        data: function () {
            return {
                result: '',
                maxDocs: '',
                query: '',
                isExact: false,
                dateFrom: '',
                dateTo: '',
                title: '',
                agency: '',
                author: '',
                FlaskAddress: "http://localhost:5000/"
            }
        },
        mounted() {
            this.$refs.query.focus();
        },
        computed: {
            isLoading() {
                return this.result == null;
            }
        },
        methods: {
            addOperator(operator) {
                this.query += " " + operator.toUpperCase() + " ";
                this.$refs.query.focus();
            },
            addField(field, value, addQuotes=true) {
                if (value.length > 0) {
                    if(addQuotes && value.lastIndexOf(" ") !== -1) {
                        value = '"' + value + '"';
                    }
                    this.query += " " + field + ":" + value;
                }
                this[field] = '';
            },
            dateToString(date) {
                date = new Date(date);
                return date.getFullYear() +
                    ('0' + (date.getMonth() + 1)).slice(-2) +
                    ('0' + date.getDate()).slice(-2);
            },
            addRange(field, start, end) {
                this.addField(field, "[" + this.dateToString(start) + " TO " + this.dateToString(end) + "]", false);
                this.dateFrom = '';
                this.dateTo = '';
            },
            resetResults() {
                this.result = '';
            },
            postQuery() {
                this.result = null;
                let this_ = this;
                $.ajax({
                    url: this.FlaskAddress,
                    type: 'GET',
                    data: {
                        query: this_.query,
                        max_docs: this_.maxDocs === '' ? -1 : this_.maxDocs
                    },
                    success: function (response) {
                        this_.result = response;
                    },
                    error: function (jqXHR, error) {
                        console.log(error);
                    }
                });
            }
        },
        watch: {
            isExact: function (value) {
                if (value) {
                    this.query = '"' + this.query + '"';
                } else if (this.query.length > 1 && this.query[0] === '"' && this.query[this.query.length - 1] === '"') {
                    this.query = this.query.slice(1, -1);
                }
            }
        }
    }
</script>

<style scoped>
    .header {
        font-size: 2em;
        color: #666161;
        grid-column: title-start / field-start;
        grid-row: header / content;
        justify-self: start;
    }

    .section {
        margin-bottom: 2em;
        display: grid;
        grid-template-columns: [title-start] 5em [field-start] 7em [date-from] 1em [date-to] 7em [add-start] 2.2em
            [add-end] minmax(5em, 0.5fr) [help-middle] minmax(10em, 0.5fr) [end];
        grid-template-rows: [header] 3.5em [content] repeat(4, 2.2em) [end];
        justify-content: start;
        grid-column-gap: 1.2em;
        grid-row-gap: 1em;
    }

    .example {
        grid-column: add-end / help-middle;
        justify-self: end;
        text-align: right;
        align-self: center;
        color: #666161;
        font-size: 0.8em;
    }

    .description {
        grid-column: help-middle / end;
        align-self: center;
        color: #666161;
        font-size: 0.8em;
    }

    .title {
        grid-column: title-start / field-start;
        justify-self: end;
        align-self: center;
    }

    .field {
        grid-column: field-start / add-start;
        place-self: stretch;
    }

    .date-from {
        grid-column: field-start / date-from;
        place-self: stretch;
    }

    .date-to {
        grid-column: date-to / add-start;
        place-self: stretch;
    }

    .date-middle {
        grid-column: date-from / date-to;
        font-size: 3em;
        color: #448AFF;
        margin-top: -0.3em;
        place-self: center;
    }

    .add {
        grid-column: add-start / add-end;
        place-self: stretch;
        font-size: 1.5em;
        border: 0;
        border-radius: 50%;
    }

    input {
        padding-left: 0.5em;
        border: 0;
        background: transparent;
        border-bottom: #82B1FF 2px solid;
        outline: none;
    }

    input:focus {
        border-bottom-color: #2962FF;
    }

    .query {
        font-size: 1.5em;
    }

    .main-section {
        width: 100%;
        display: grid;
        grid-template-columns: [start] auto repeat(3, 5em) [max-start] auto [max-end] 1fr [end];
        grid-template-rows: [input-start] 3em [options-start] auto [end];
        justify-content: start;
        grid-column-gap: 1em;
        grid-row-gap: 1em;
        margin-bottom: 2em;
    }

    .query {
        grid-column: start / end;
        grid-row: input-start / options-start;
        justify-self: stretch;
    }

    .option {
        grid-row: options-start / end;
        place-self: stretch;
        padding: 0.5em 1em;
        border-radius: 5px;
    }

    .short {
        align-self: center;
    }

    .short > input {
        width: 2em;
        margin: 0 0.2em;
    }

    .button {
        text-align: center;
        background-color: #448AFF;
        color: #fff;
        cursor: pointer;
    }

    .submit {
        width: 7em;
        background-color: #448AFF;
        padding: 0.5em 0.5em 0.5em 0.3em;
        border-radius: 5px;
    }

    .results {
        margin-bottom: 2em;
    }

    .results-header {
        font-size: 2em;
        color: #666161;
    }

    .results-subheader {
        color: #969191;
        margin-bottom: 0.5em;
    }

    .results-title {
        font-size: 1.5em;
    }

    .results-text {
        color: #666161;
        margin-bottom: 1em;
    }

</style>

<style>
    .match {
        color: #0D47A1;
        font-weight: bold;
    }
</style>
