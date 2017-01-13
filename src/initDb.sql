CREATE TABLE stocks (
    ticker character varying(10) NOT NULL,
    open real NOT NULL,
    close real NOT NULL,
    low real NOT NULL,
    high real NOT NULL,
    volume integer NOT NULL,
    adj_close real NOT NULL,
    id integer NOT NULL,
    "timestamp" date
);


ALTER TABLE stocks OWNER TO postgres;

--
-- Name: stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE stocks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE stocks_id_seq OWNER TO postgres;

--
-- Name: stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE stocks_id_seq OWNED BY stocks.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY stocks ALTER COLUMN id SET DEFAULT nextval('stocks_id_seq'::regclass);


--
-- Name: unique_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY stocks
    ADD CONSTRAINT unique_pkey UNIQUE (id);


--
-- PostgreSQL database dump complete
--
