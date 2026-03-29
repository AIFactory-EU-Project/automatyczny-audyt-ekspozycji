SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = heap;


drop database if exists planogram_test;
drop user if exists planogram_test;
create user planogram_test password 'planogram_test';
create database planogram_test;
alter database planogram_test owner to planogram_test;
GRANT postgres TO planogram_test;
\c planogram_test





--
-- Name: access_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.access_token (
    id integer NOT NULL,
    client_id integer NOT NULL,
    user_id integer,
    token character varying(255) NOT NULL,
    expires_at integer,
    scope character varying(255) DEFAULT NULL::character varying
);


ALTER TABLE public.access_token OWNER TO postgres;

--
-- Name: access_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.access_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.access_token_id_seq OWNER TO postgres;

--
-- Name: auth_code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_code (
    id integer NOT NULL,
    client_id integer NOT NULL,
    user_id integer,
    token character varying(255) NOT NULL,
    redirect_uri text NOT NULL,
    expires_at integer,
    scope character varying(255) DEFAULT NULL::character varying
);


ALTER TABLE public.auth_code OWNER TO postgres;

--
-- Name: auth_code_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_code_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_code_id_seq OWNER TO postgres;

--
-- Name: camera; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.camera (
    id integer NOT NULL,
    segment_id integer,
    shop_id integer,
    type character varying(255) NOT NULL,
    ip character varying(20) NOT NULL,
    manipulation_settings text NOT NULL
);


ALTER TABLE public.camera OWNER TO postgres;

--
-- Name: camera_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.camera_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.camera_id_seq OWNER TO postgres;

--
-- Name: client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client (
    id integer NOT NULL,
    random_id character varying(255) NOT NULL,
    redirect_uris text NOT NULL,
    secret character varying(255) NOT NULL,
    allowed_grant_types text NOT NULL
);


ALTER TABLE public.client OWNER TO postgres;

--
-- Name: COLUMN client.redirect_uris; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.client.redirect_uris IS '(DC2Type:array)';


--
-- Name: COLUMN client.allowed_grant_types; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.client.allowed_grant_types IS '(DC2Type:array)';


--
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_id_seq OWNER TO postgres;

--
-- Name: failed_import_attempt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.failed_import_attempt (
    id integer NOT NULL,
    camera_id integer,
    attempt_date timestamp(0) without time zone NOT NULL,
    reason text
);


ALTER TABLE public.failed_import_attempt OWNER TO postgres;

--
-- Name: failed_import_attempt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.failed_import_attempt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.failed_import_attempt_id_seq OWNER TO postgres;

--
-- Name: file; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.file (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    directory text NOT NULL,
    extension character varying(10) DEFAULT NULL::character varying,
    storage_location character varying(120) NOT NULL,
    temporary boolean NOT NULL
);


ALTER TABLE public.file OWNER TO postgres;

--
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.file_id_seq OWNER TO postgres;

--
-- Name: fos_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fos_user (
    id integer NOT NULL,
    username character varying(180) NOT NULL,
    username_canonical character varying(180) NOT NULL,
    email character varying(180) NOT NULL,
    email_canonical character varying(180) NOT NULL,
    enabled boolean NOT NULL,
    salt character varying(255) DEFAULT NULL::character varying,
    password character varying(255) NOT NULL,
    last_login timestamp(0) without time zone DEFAULT NULL::timestamp without time zone,
    confirmation_token character varying(180) DEFAULT NULL::character varying,
    password_requested_at timestamp(0) without time zone DEFAULT NULL::timestamp without time zone,
    roles text NOT NULL
);


ALTER TABLE public.fos_user OWNER TO postgres;

--
-- Name: COLUMN fos_user.roles; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.fos_user.roles IS '(DC2Type:array)';


--
-- Name: fos_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fos_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fos_user_id_seq OWNER TO postgres;

--
-- Name: import; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.import (
    id integer NOT NULL,
    date_time timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_complete boolean DEFAULT false NOT NULL
);


ALTER TABLE public.import OWNER TO postgres;

--
-- Name: import_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.import_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.import_id_seq OWNER TO postgres;

--
-- Name: migration_versions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.migration_versions (
    version character varying(14) NOT NULL,
    executed_at timestamp(0) without time zone NOT NULL
);


ALTER TABLE public.migration_versions OWNER TO postgres;

--
-- Name: COLUMN migration_versions.executed_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.migration_versions.executed_at IS '(DC2Type:datetime_immutable)';


--
-- Name: photo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photo (
    id integer NOT NULL,
    camera_id integer,
    "time" timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    storage_id character varying(255) NOT NULL,
    storage_type character varying(255) NOT NULL,
    is_ai_processed boolean NOT NULL,
    is_manipulated boolean NOT NULL,
    is_valid boolean NOT NULL,
    CONSTRAINT photo_storage_type_check CHECK (((storage_type)::text = ANY ((ARRAY['LOCAL'::character varying, 'GOOGLE_CLOUD_STORAGE'::character varying])::text[])))
);


ALTER TABLE public.photo OWNER TO postgres;

--
-- Name: COLUMN photo.storage_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.photo.storage_type IS '(DC2Type:FileStorageType)';


--
-- Name: photo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.photo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.photo_id_seq OWNER TO postgres;

--
-- Name: planogram; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planogram (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255) NOT NULL,
    neural_network_id integer NOT NULL,
    version character varying(255) NOT NULL
);


ALTER TABLE public.planogram OWNER TO postgres;

--
-- Name: planogram_element; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planogram_element (
    id integer NOT NULL,
    planogram_id integer,
    sku_id integer,
    shelf integer NOT NULL,
    "position" integer NOT NULL,
    faces_count integer NOT NULL,
    stack_count integer NOT NULL
);


ALTER TABLE public.planogram_element OWNER TO postgres;

--
-- Name: planogram_element_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planogram_element_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planogram_element_id_seq OWNER TO postgres;

--
-- Name: planogram_element_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planogram_element_id_seq OWNED BY public.planogram_element.id;


--
-- Name: planogram_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planogram_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planogram_id_seq OWNER TO postgres;

--
-- Name: planogram_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planogram_id_seq OWNED BY public.planogram.id;


--
-- Name: refresh_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refresh_token (
    id integer NOT NULL,
    client_id integer NOT NULL,
    user_id integer,
    token character varying(255) NOT NULL,
    expires_at integer,
    scope character varying(255) DEFAULT NULL::character varying
);


ALTER TABLE public.refresh_token OWNER TO postgres;

--
-- Name: refresh_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.refresh_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.refresh_token_id_seq OWNER TO postgres;

--
-- Name: report_photo_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_photo_analysis (
    id integer NOT NULL,
    planogram_id integer,
    photo_id integer,
    date_time timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data json NOT NULL
);


ALTER TABLE public.report_photo_analysis OWNER TO postgres;

--
-- Name: report_photo_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_photo_analysis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_photo_analysis_id_seq OWNER TO postgres;

--
-- Name: segment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.segment (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    CONSTRAINT segment_type_check CHECK (((type)::text = ANY ((ARRAY['READY_MEAL'::character varying, 'QUICK_SNACK'::character varying, 'GRILL'::character varying])::text[])))
);


ALTER TABLE public.segment OWNER TO postgres;

--
-- Name: COLUMN segment.type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.segment.type IS '(DC2Type:SegmentType)';


--
-- Name: segment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.segment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.segment_id_seq OWNER TO postgres;

--
-- Name: shop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(255) NOT NULL
);


ALTER TABLE public.shop OWNER TO postgres;

--
-- Name: shop_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shop_id_seq OWNER TO postgres;

--
-- Name: shop_planogram_assignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_planogram_assignment (
    id integer NOT NULL,
    segment_id integer,
    shop_id integer,
    planogram_id integer,
    start_date_time timestamp(0) without time zone NOT NULL,
    end_date_time timestamp(0) without time zone NOT NULL
);


ALTER TABLE public.shop_planogram_assignment OWNER TO postgres;

--
-- Name: shop_planogram_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_planogram_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shop_planogram_assignment_id_seq OWNER TO postgres;

--
-- Name: shop_planogram_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_planogram_assignment_id_seq OWNED BY public.shop_planogram_assignment.id;


--
-- Name: sku; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sku (
    id integer NOT NULL,
    file_id integer,
    name character varying(255) NOT NULL,
    index character varying(255) NOT NULL
);


ALTER TABLE public.sku OWNER TO postgres;

--
-- Name: sku_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sku_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sku_id_seq OWNER TO postgres;

--
-- Name: sku_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sku_id_seq OWNED BY public.sku.id;


--
-- Name: planogram id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram ALTER COLUMN id SET DEFAULT nextval('public.planogram_id_seq'::regclass);


--
-- Name: planogram_element id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram_element ALTER COLUMN id SET DEFAULT nextval('public.planogram_element_id_seq'::regclass);


--
-- Name: shop_planogram_assignment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_planogram_assignment ALTER COLUMN id SET DEFAULT nextval('public.shop_planogram_assignment_id_seq'::regclass);


--
-- Name: sku id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sku ALTER COLUMN id SET DEFAULT nextval('public.sku_id_seq'::regclass);


--
-- Name: access_token access_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_token
    ADD CONSTRAINT access_token_pkey PRIMARY KEY (id);


--
-- Name: auth_code auth_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_code
    ADD CONSTRAINT auth_code_pkey PRIMARY KEY (id);


--
-- Name: camera camera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.camera
    ADD CONSTRAINT camera_pkey PRIMARY KEY (id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: failed_import_attempt failed_import_attempt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.failed_import_attempt
    ADD CONSTRAINT failed_import_attempt_pkey PRIMARY KEY (id);


--
-- Name: file file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- Name: fos_user fos_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fos_user
    ADD CONSTRAINT fos_user_pkey PRIMARY KEY (id);


--
-- Name: import import_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.import
    ADD CONSTRAINT import_pkey PRIMARY KEY (id);


--
-- Name: migration_versions migration_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.migration_versions
    ADD CONSTRAINT migration_versions_pkey PRIMARY KEY (version);


--
-- Name: photo photo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photo
    ADD CONSTRAINT photo_pkey PRIMARY KEY (id);


--
-- Name: planogram_element planogram_element_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram_element
    ADD CONSTRAINT planogram_element_pkey PRIMARY KEY (id);


--
-- Name: planogram planogram_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram
    ADD CONSTRAINT planogram_pkey PRIMARY KEY (id);


--
-- Name: refresh_token refresh_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_pkey PRIMARY KEY (id);


--
-- Name: report_photo_analysis report_photo_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_photo_analysis
    ADD CONSTRAINT report_photo_analysis_pkey PRIMARY KEY (id);


--
-- Name: segment segment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.segment
    ADD CONSTRAINT segment_pkey PRIMARY KEY (id);


--
-- Name: shop shop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_pkey PRIMARY KEY (id);


--
-- Name: shop_planogram_assignment shop_planogram_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_planogram_assignment
    ADD CONSTRAINT shop_planogram_assignment_pkey PRIMARY KEY (id);


--
-- Name: sku sku_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sku
    ADD CONSTRAINT sku_pkey PRIMARY KEY (id);


--
-- Name: idx_14b78418b47685cd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_14b78418b47685cd ON public.photo USING btree (camera_id);


--
-- Name: idx_3b1cee054d16c4dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_3b1cee054d16c4dd ON public.camera USING btree (shop_id);


--
-- Name: idx_3b1cee05db296aad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_3b1cee05db296aad ON public.camera USING btree (segment_id);


--
-- Name: idx_5933d02c19eb6921; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_5933d02c19eb6921 ON public.auth_code USING btree (client_id);


--
-- Name: idx_5933d02ca76ed395; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_5933d02ca76ed395 ON public.auth_code USING btree (user_id);


--
-- Name: idx_9f9f2d6d1777d41c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_9f9f2d6d1777d41c ON public.planogram_element USING btree (sku_id);


--
-- Name: idx_9f9f2d6d5afb77ab; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_9f9f2d6d5afb77ab ON public.planogram_element USING btree (planogram_id);


--
-- Name: idx_aaf32b454d16c4dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_aaf32b454d16c4dd ON public.shop_planogram_assignment USING btree (shop_id);


--
-- Name: idx_aaf32b455afb77ab; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_aaf32b455afb77ab ON public.shop_planogram_assignment USING btree (planogram_id);


--
-- Name: idx_aaf32b45db296aad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_aaf32b45db296aad ON public.shop_planogram_assignment USING btree (segment_id);


--
-- Name: idx_b6a2dd6819eb6921; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_b6a2dd6819eb6921 ON public.access_token USING btree (client_id);


--
-- Name: idx_b6a2dd68a76ed395; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_b6a2dd68a76ed395 ON public.access_token USING btree (user_id);


--
-- Name: idx_bae35ae4b47685cd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_bae35ae4b47685cd ON public.failed_import_attempt USING btree (camera_id);


--
-- Name: idx_c38374c75afb77ab; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_c38374c75afb77ab ON public.report_photo_analysis USING btree (planogram_id);


--
-- Name: idx_c38374c77e9e4c8c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_c38374c77e9e4c8c ON public.report_photo_analysis USING btree (photo_id);


--
-- Name: idx_c74f219519eb6921; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_c74f219519eb6921 ON public.refresh_token USING btree (client_id);


--
-- Name: idx_c74f2195a76ed395; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_c74f2195a76ed395 ON public.refresh_token USING btree (user_id);


--
-- Name: idx_f9038c493cb796c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_f9038c493cb796c ON public.sku USING btree (file_id);


--
-- Name: uniq_5933d02c5f37a13b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_5933d02c5f37a13b ON public.auth_code USING btree (token);


--
-- Name: uniq_957a647992fc23a8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_957a647992fc23a8 ON public.fos_user USING btree (username_canonical);


--
-- Name: uniq_957a6479a0d96fbf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_957a6479a0d96fbf ON public.fos_user USING btree (email_canonical);


--
-- Name: uniq_957a6479c05fb297; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_957a6479c05fb297 ON public.fos_user USING btree (confirmation_token);


--
-- Name: uniq_b6a2dd685f37a13b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_b6a2dd685f37a13b ON public.access_token USING btree (token);


--
-- Name: uniq_c74f21955f37a13b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uniq_c74f21955f37a13b ON public.refresh_token USING btree (token);


--
-- Name: photo fk_14b78418b47685cd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photo
    ADD CONSTRAINT fk_14b78418b47685cd FOREIGN KEY (camera_id) REFERENCES public.camera(id);


--
-- Name: camera fk_3b1cee054d16c4dd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.camera
    ADD CONSTRAINT fk_3b1cee054d16c4dd FOREIGN KEY (shop_id) REFERENCES public.shop(id);


--
-- Name: camera fk_3b1cee05db296aad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.camera
    ADD CONSTRAINT fk_3b1cee05db296aad FOREIGN KEY (segment_id) REFERENCES public.segment(id);


--
-- Name: auth_code fk_5933d02c19eb6921; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_code
    ADD CONSTRAINT fk_5933d02c19eb6921 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: auth_code fk_5933d02ca76ed395; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_code
    ADD CONSTRAINT fk_5933d02ca76ed395 FOREIGN KEY (user_id) REFERENCES public.fos_user(id) ON DELETE CASCADE;


--
-- Name: planogram_element fk_9f9f2d6d1777d41c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram_element
    ADD CONSTRAINT fk_9f9f2d6d1777d41c FOREIGN KEY (sku_id) REFERENCES public.sku(id);


--
-- Name: planogram_element fk_9f9f2d6d5afb77ab; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planogram_element
    ADD CONSTRAINT fk_9f9f2d6d5afb77ab FOREIGN KEY (planogram_id) REFERENCES public.planogram(id);


--
-- Name: shop_planogram_assignment fk_aaf32b454d16c4dd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_planogram_assignment
    ADD CONSTRAINT fk_aaf32b454d16c4dd FOREIGN KEY (shop_id) REFERENCES public.shop(id);


--
-- Name: shop_planogram_assignment fk_aaf32b455afb77ab; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_planogram_assignment
    ADD CONSTRAINT fk_aaf32b455afb77ab FOREIGN KEY (planogram_id) REFERENCES public.planogram(id);


--
-- Name: shop_planogram_assignment fk_aaf32b45db296aad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_planogram_assignment
    ADD CONSTRAINT fk_aaf32b45db296aad FOREIGN KEY (segment_id) REFERENCES public.segment(id);


--
-- Name: access_token fk_b6a2dd6819eb6921; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_token
    ADD CONSTRAINT fk_b6a2dd6819eb6921 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: access_token fk_b6a2dd68a76ed395; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_token
    ADD CONSTRAINT fk_b6a2dd68a76ed395 FOREIGN KEY (user_id) REFERENCES public.fos_user(id) ON DELETE CASCADE;


--
-- Name: failed_import_attempt fk_bae35ae4b47685cd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.failed_import_attempt
    ADD CONSTRAINT fk_bae35ae4b47685cd FOREIGN KEY (camera_id) REFERENCES public.camera(id);


--
-- Name: report_photo_analysis fk_c38374c75afb77ab; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_photo_analysis
    ADD CONSTRAINT fk_c38374c75afb77ab FOREIGN KEY (planogram_id) REFERENCES public.planogram(id);


--
-- Name: report_photo_analysis fk_c38374c77e9e4c8c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_photo_analysis
    ADD CONSTRAINT fk_c38374c77e9e4c8c FOREIGN KEY (photo_id) REFERENCES public.photo(id);


--
-- Name: refresh_token fk_c74f219519eb6921; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT fk_c74f219519eb6921 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: refresh_token fk_c74f2195a76ed395; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT fk_c74f2195a76ed395 FOREIGN KEY (user_id) REFERENCES public.fos_user(id) ON DELETE CASCADE;


--
-- Name: sku fk_f9038c493cb796c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sku
    ADD CONSTRAINT fk_f9038c493cb796c FOREIGN KEY (file_id) REFERENCES public.file(id);



GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO planogram_test;