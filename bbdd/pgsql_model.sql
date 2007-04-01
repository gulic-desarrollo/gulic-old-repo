--
-- PostgreSQL database dump
--

SET client_encoding = 'LATIN1';
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.webusers DROP CONSTRAINT webusers_people_fk;
ALTER TABLE ONLY public.quota DROP CONSTRAINT quota_quotatype_fk;
ALTER TABLE ONLY public.quota DROP CONSTRAINT quota_partnertype_fk;
ALTER TABLE ONLY public.quota DROP CONSTRAINT quota_partner_fk;
ALTER TABLE ONLY public.partner DROP CONSTRAINT partner_people_fk;
ALTER TABLE ONLY public.mailusers DROP CONSTRAINT mailusers_people_fk;
ALTER TABLE ONLY public.jabberusers DROP CONSTRAINT jabberusers_people_fk;
ALTER TABLE ONLY public.im DROP CONSTRAINT im_people_fk;
ALTER TABLE ONLY public.im DROP CONSTRAINT im_fk;
ALTER TABLE ONLY public.ftpusers DROP CONSTRAINT ftpusers_people_fk;
ALTER TABLE ONLY public.charge DROP CONSTRAINT charge_partner_fk;
ALTER TABLE ONLY public.charge DROP CONSTRAINT charge_chargetype_fk;
ALTER TABLE ONLY public.webusers DROP CONSTRAINT webusers_pk;
ALTER TABLE ONLY public.quotatype DROP CONSTRAINT quotatype_uk;
ALTER TABLE ONLY public.quotatype DROP CONSTRAINT quotatype_pk;
ALTER TABLE ONLY public.quota DROP CONSTRAINT quota_uk;
ALTER TABLE ONLY public.quota DROP CONSTRAINT quota_pk;
ALTER TABLE ONLY public.people DROP CONSTRAINT people_uk;
ALTER TABLE ONLY public.partnertype DROP CONSTRAINT partnertype_uk;
ALTER TABLE ONLY public.partnertype DROP CONSTRAINT partnertype_pk;
ALTER TABLE ONLY public.partner DROP CONSTRAINT partner_uk;
ALTER TABLE ONLY public.partner DROP CONSTRAINT partner_pk;
ALTER TABLE ONLY public.mailusers DROP CONSTRAINT mailusers_pk;
ALTER TABLE ONLY public.jabberusers DROP CONSTRAINT jabberusers_pk;
ALTER TABLE ONLY public.imtype DROP CONSTRAINT imtype_uk;
ALTER TABLE ONLY public.imtype DROP CONSTRAINT imtype_pk;
ALTER TABLE ONLY public.im DROP CONSTRAINT im_uk;
ALTER TABLE ONLY public.im DROP CONSTRAINT im_pk;
ALTER TABLE ONLY public.ftpusers DROP CONSTRAINT ftpusers_pk;
ALTER TABLE ONLY public.chargetype DROP CONSTRAINT chargetype_pk;
ALTER TABLE ONLY public.charge DROP CONSTRAINT charge_pk;
DROP TABLE public.webusers;
DROP SEQUENCE public.users_id_seq;
DROP TABLE public.quotatype;
DROP SEQUENCE public.quotatype_id_seq;
DROP TABLE public.quota;
DROP SEQUENCE public.quota_id_seq;
DROP TABLE public.people;
DROP SEQUENCE public.people_id_seq;
DROP TABLE public.partnertype;
DROP SEQUENCE public.partnertype_id_seq;
DROP TABLE public.partner;
DROP SEQUENCE public.partner_id_seq;
DROP TABLE public.mailusers;
DROP TABLE public.jabberusers;
DROP TABLE public.imtype;
DROP SEQUENCE public.imtype_id_seq;
DROP TABLE public.im;
DROP SEQUENCE public.im_id_seq;
DROP TABLE public.ftpusers;
DROP TABLE public.chargetype;
DROP TABLE public.charge;
DROP PROCEDURAL LANGUAGE plpythonu;
DROP PROCEDURAL LANGUAGE plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'Standard public schema';


--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: 
--

CREATE PROCEDURAL LANGUAGE plpgsql;


--
-- Name: plpythonu; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: 
--

CREATE PROCEDURAL LANGUAGE plpythonu;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: charge; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE charge (
    id serial NOT NULL,
    ref_idchargetype integer NOT NULL,
    init_of_period date NOT NULL,
    end_of_period date NOT NULL,
    ref_idpartner integer
);


ALTER TABLE public.charge OWNER TO lcabrera;

--
-- Name: charge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('charge', 'id'), 1, false);


--
-- Name: chargetype; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE chargetype (
    id serial NOT NULL,
    description character varying(200),
    duration integer DEFAULT 12,
    warning_time integer DEFAULT 1
);


ALTER TABLE public.chargetype OWNER TO lcabrera;

--
-- Name: chargetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('chargetype', 'id'), 1, false);


--
-- Name: ftpusers; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE ftpusers (
    id serial NOT NULL,
    ref_idpeople integer DEFAULT 1 NOT NULL,
    nick character varying(20) NOT NULL,
    pass character varying(8) NOT NULL,
    init_date date NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.ftpusers OWNER TO lcabrera;

--
-- Name: ftpusers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('ftpusers', 'id'), 1, false);


--
-- Name: im_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE im_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.im_id_seq OWNER TO lcabrera;

--
-- Name: im_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('im_id_seq', 1, false);


--
-- Name: im; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE im (
    id integer DEFAULT nextval('im_id_seq'::regclass) NOT NULL,
    ref_idpeople integer NOT NULL,
    ref_idimtype integer NOT NULL,
    data character varying(250) NOT NULL,
    ispreferred boolean DEFAULT false
);


ALTER TABLE public.im OWNER TO lcabrera;

--
-- Name: imtype_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE imtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.imtype_id_seq OWNER TO lcabrera;

--
-- Name: imtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('imtype_id_seq', 1, false);


--
-- Name: imtype; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE imtype (
    id integer DEFAULT nextval('imtype_id_seq'::regclass) NOT NULL,
    description character varying(250),
    ispreferred boolean DEFAULT false
);


ALTER TABLE public.imtype OWNER TO lcabrera;

--
-- Name: jabberusers; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE jabberusers (
    id serial NOT NULL,
    ref_idpeople integer DEFAULT 1 NOT NULL,
    nick character varying(20) NOT NULL,
    pass character varying(8) NOT NULL,
    init_date date NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.jabberusers OWNER TO lcabrera;

--
-- Name: jabberusers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('jabberusers', 'id'), 1, false);


--
-- Name: mailusers; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE mailusers (
    id serial NOT NULL,
    ref_idpeople integer DEFAULT 1 NOT NULL,
    nick character varying(20) NOT NULL,
    pass character varying(8) NOT NULL,
    init_date date NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.mailusers OWNER TO lcabrera;

--
-- Name: mailusers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('mailusers', 'id'), 1, false);


--
-- Name: partner_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.partner_id_seq OWNER TO lcabrera;

--
-- Name: partner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('partner_id_seq', 1, false);


--
-- Name: partner; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE partner (
    id integer DEFAULT nextval('partner_id_seq'::regclass) NOT NULL,
    ref_idusers integer NOT NULL,
    ref_idpeople integer NOT NULL,
    partner boolean DEFAULT false NOT NULL
);


ALTER TABLE public.partner OWNER TO lcabrera;

--
-- Name: partnertype_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE partnertype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.partnertype_id_seq OWNER TO lcabrera;

--
-- Name: partnertype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('partnertype_id_seq', 1, false);


--
-- Name: partnertype; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE partnertype (
    id integer DEFAULT nextval('partnertype_id_seq'::regclass) NOT NULL,
    description character varying(50) NOT NULL
);


ALTER TABLE public.partnertype OWNER TO lcabrera;

--
-- Name: people_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE people_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.people_id_seq OWNER TO lcabrera;

--
-- Name: people_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('people_id_seq', 1, false);


--
-- Name: people; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE people (
    id integer DEFAULT nextval('people_id_seq'::regclass) NOT NULL,
    firstname character varying(40) NOT NULL,
    lastname character varying(40) DEFAULT ''::character varying,
    surname character varying(200) NOT NULL,
    nif character varying(9) DEFAULT 'xxxxxxxxx'::character varying,
    dateofbirth date
);


ALTER TABLE public.people OWNER TO lcabrera;

--
-- Name: quota_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE quota_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.quota_id_seq OWNER TO lcabrera;

--
-- Name: quota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('quota_id_seq', 1, false);


--
-- Name: quota; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE quota (
    id integer DEFAULT nextval('quota_id_seq'::regclass) NOT NULL,
    ref_idpartner integer NOT NULL,
    ref_partnertype integer DEFAULT 1 NOT NULL,
    payment_date date NOT NULL,
    end_of_period date NOT NULL,
    ref_idquotatype integer DEFAULT 1
);


ALTER TABLE public.quota OWNER TO lcabrera;

--
-- Name: quotatype_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE quotatype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.quotatype_id_seq OWNER TO lcabrera;

--
-- Name: quotatype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('quotatype_id_seq', 1, false);


--
-- Name: quotatype; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE quotatype (
    id integer DEFAULT nextval('quotatype_id_seq'::regclass) NOT NULL,
    description character varying(200),
    duration integer DEFAULT 12,
    warning_time integer DEFAULT 1
);


ALTER TABLE public.quotatype OWNER TO lcabrera;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: lcabrera
--

CREATE SEQUENCE users_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO lcabrera;

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval('users_id_seq', 1, true);


--
-- Name: webusers; Type: TABLE; Schema: public; Owner: lcabrera; Tablespace: 
--

CREATE TABLE webusers (
    id serial NOT NULL,
    ref_idpeople integer DEFAULT 1 NOT NULL,
    nick character varying(20) NOT NULL,
    pass character varying(8) NOT NULL,
    init_date date NOT NULL,
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.webusers OWNER TO lcabrera;

--
-- Name: webusers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lcabrera
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('webusers', 'id'), 1, false);


--
-- Data for Name: charge; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: chargetype; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: ftpusers; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: im; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: imtype; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: jabberusers; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: mailusers; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: partner; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: partnertype; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: people; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: quota; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: quotatype; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Data for Name: webusers; Type: TABLE DATA; Schema: public; Owner: lcabrera
--



--
-- Name: charge_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY charge
    ADD CONSTRAINT charge_pk PRIMARY KEY (id);


--
-- Name: chargetype_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY chargetype
    ADD CONSTRAINT chargetype_pk PRIMARY KEY (id);


--
-- Name: ftpusers_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY ftpusers
    ADD CONSTRAINT ftpusers_pk PRIMARY KEY (id);


--
-- Name: im_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY im
    ADD CONSTRAINT im_pk PRIMARY KEY (id);


--
-- Name: im_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY im
    ADD CONSTRAINT im_uk UNIQUE (id);


--
-- Name: imtype_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY imtype
    ADD CONSTRAINT imtype_pk PRIMARY KEY (id);


--
-- Name: imtype_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY imtype
    ADD CONSTRAINT imtype_uk UNIQUE (id);


--
-- Name: jabberusers_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY jabberusers
    ADD CONSTRAINT jabberusers_pk PRIMARY KEY (id);


--
-- Name: mailusers_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY mailusers
    ADD CONSTRAINT mailusers_pk PRIMARY KEY (id);


--
-- Name: partner_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY partner
    ADD CONSTRAINT partner_pk PRIMARY KEY (id);


--
-- Name: partner_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY partner
    ADD CONSTRAINT partner_uk UNIQUE (id);


--
-- Name: partnertype_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY partnertype
    ADD CONSTRAINT partnertype_pk PRIMARY KEY (id);


--
-- Name: partnertype_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY partnertype
    ADD CONSTRAINT partnertype_uk UNIQUE (id);


--
-- Name: people_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY people
    ADD CONSTRAINT people_uk UNIQUE (id);


--
-- Name: quota_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY quota
    ADD CONSTRAINT quota_pk PRIMARY KEY (id);


--
-- Name: quota_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY quota
    ADD CONSTRAINT quota_uk UNIQUE (id);


--
-- Name: quotatype_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY quotatype
    ADD CONSTRAINT quotatype_pk PRIMARY KEY (id);


--
-- Name: quotatype_uk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY quotatype
    ADD CONSTRAINT quotatype_uk UNIQUE (id);


--
-- Name: webusers_pk; Type: CONSTRAINT; Schema: public; Owner: lcabrera; Tablespace: 
--

ALTER TABLE ONLY webusers
    ADD CONSTRAINT webusers_pk PRIMARY KEY (id);


--
-- Name: charge_chargetype_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY charge
    ADD CONSTRAINT charge_chargetype_fk FOREIGN KEY (ref_idchargetype) REFERENCES chargetype(id);


--
-- Name: charge_partner_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY charge
    ADD CONSTRAINT charge_partner_fk FOREIGN KEY (ref_idpartner) REFERENCES partner(id);


--
-- Name: ftpusers_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY ftpusers
    ADD CONSTRAINT ftpusers_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: im_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY im
    ADD CONSTRAINT im_fk FOREIGN KEY (ref_idimtype) REFERENCES imtype(id);


--
-- Name: im_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY im
    ADD CONSTRAINT im_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: jabberusers_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY jabberusers
    ADD CONSTRAINT jabberusers_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: mailusers_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY mailusers
    ADD CONSTRAINT mailusers_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: partner_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY partner
    ADD CONSTRAINT partner_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: quota_partner_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY quota
    ADD CONSTRAINT quota_partner_fk FOREIGN KEY (ref_idpartner) REFERENCES partner(id);


--
-- Name: quota_partnertype_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY quota
    ADD CONSTRAINT quota_partnertype_fk FOREIGN KEY (ref_partnertype) REFERENCES partnertype(id);


--
-- Name: quota_quotatype_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY quota
    ADD CONSTRAINT quota_quotatype_fk FOREIGN KEY (ref_idquotatype) REFERENCES quotatype(id);


--
-- Name: webusers_people_fk; Type: FK CONSTRAINT; Schema: public; Owner: lcabrera
--

ALTER TABLE ONLY webusers
    ADD CONSTRAINT webusers_people_fk FOREIGN KEY (ref_idpeople) REFERENCES people(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

