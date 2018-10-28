<template>
    <div v-if="!isLoading && result.length === 0">
        <div class="main-section">
            <input class="query" v-model="query" ref="query" placeholder="Search..."/>
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

            <div class="title">Title</div>
            <input v-model="title" @keyup.enter="addField('title', title)" class="field" placeholder="E.g. Trump"/>
            <button class="button add" @click="addField('title', title)">+</button>

            <div class="title">Agency</div>
            <input v-model="agency" @keyup.enter="addField('agency', agency)" class="field" placeholder="E.g. Reuters"/>
            <button class="button add" @click="addField('agency', agency)">+</button>

            <div class="title">Author</div>
            <input v-model="author" @keyup.enter="addField('author', author)" class="field" placeholder="E.g. Stempel"/>
            <div class="button add" @click="addField('author', author)">+</div>
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
                    <a :href="document.path">{{ document.filename }}</a>
                </div>
                <div class="results-text">{{ document.text }}</div>
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
            }
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
            addField(field, value) {
                if (value.length > 0) {
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
                this.addField(field, "[" + this.dateToString(start) + " TO " + this.dateToString(end) + "]");
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
                    url: 'test.json',
                    type: 'GET',
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
        grid-template-columns: [title-start] 5em [field-start] 9em [date-from] 1em [date-to] 9em [add-start] 2.2em [end];
        grid-template-rows: [header] 3.5em [content] repeat(4, 2.2em);
        justify-content: start;
        grid-column-gap: 1.5em;
        grid-row-gap: 1em;
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
        grid-column: add-start / end;
        place-self: stretch;
        font-size: 1.5em;
        border: 0;
        border-radius: 50%;
    }

    input {
        padding-left: 0.5em;
        border: 0;
        border-radius: 5px;
    }

    .query {
        font-size: 1.5em;
    }

    .main-section {
        width: 100%;
        display: grid;
        grid-template-columns: [start] auto repeat(2, 5em) [max-start] auto [max-end] 1fr [end];
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
        place-self: start;
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
