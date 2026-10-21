import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import { SearchProvider, SearchBox, Results, PagingInfo, Paging, useSearch } from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions",
});

const config = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  searchQuery: {
    search_fields: { generated_text: { weight: 3 }, age: {}, gender: {}, accent: {} },
    result_fields: {
      generated_text: { raw: {} },
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
    },
  },
};

// Fixed checkbox options (values as they appear in the Common Voice data)
const GENDERS = ["male", "female", "other"];
const AGES = ["teens", "twenties", "thirties", "fourties", "fifties", "sixties", "seventies", "eighties"];
const ACCENTS = ["us", "england", "australia", "canada", "indian", "scotland", "ireland", "african", "newzealand", "wales", "malaysia", "philippines", "singapore"];
const DURATIONS = [
  { name: "Under 3s", from: 0, to: 3 },
  { name: "3 to 6s", from: 3, to: 6 },
  { name: "6s and over", from: 6 },
];

// A simple list of checkboxes that adds/removes a filter when ticked
function CheckboxFilter({ label, field, options }) {
  const { filters, addFilter, removeFilter } = useSearch();
  const selected = filters.find((f) => f.field === field)?.values || [];

  return (
    <div style={{ marginBottom: 20 }}>
      <strong>{label}</strong>
      {options.map((option) => {
        const name = option.name || option;
        const checked = selected.some((v) => (v.name || v) === name);
        return (
          <label key={name} style={{ display: "block" }}>
            <input
              type="checkbox"
              checked={checked}
              onChange={() =>
                checked
                  ? removeFilter(field, selected.find((v) => (v.name || v) === name), "any")
                  : addFilter(field, option, "any")
              }
            />{" "}
            {name}
          </label>
        );
      })}
    </div>
  );
}

export default function App() {
  return (
    <SearchProvider config={config}>
      <Layout
        header={<SearchBox />}
        sideContent={
          <>
            <CheckboxFilter label="Gender" field="gender.keyword" options={GENDERS} />
            <CheckboxFilter label="Age" field="age.keyword" options={AGES} />
            <CheckboxFilter label="Accent" field="accent.keyword" options={ACCENTS} />
            <CheckboxFilter label="Duration" field="duration" options={DURATIONS} />
          </>
        }
        bodyHeader={<PagingInfo />}
        bodyContent={<Results titleField="generated_text" />}
        bodyFooter={<Paging />}
      />
    </SearchProvider>
  );
}