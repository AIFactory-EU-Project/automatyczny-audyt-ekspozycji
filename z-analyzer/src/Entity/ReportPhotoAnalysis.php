<?php

namespace App\Entity;

use App\Utility\DataObject\GrillReport;
use App\Utility\DataObject\PlanogramReport;
use App\Utility\DBAL\Type\SegmentType;
use DateTime;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ReportPhotoAnalysisRepository")
 */
class ReportPhotoAnalysis
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Planogram", inversedBy="reportPhotoAnalyses")
     * @ORM\JoinColumn(name="planogram_id", referencedColumnName="id", nullable=true)
     */
    private $planogram;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Photo", inversedBy="reportPhotoAnalyses")
     * @ORM\JoinColumn(name="photo_id", referencedColumnName="id")
     */
    private $photo;

    /**
     * @ORM\Column(type="datetime", options={"default": "CURRENT_TIMESTAMP"})
     */
    private $dateTime;

    /**
     * @ORM\Column(type="json")
     */
    private $data;

    /**
     * @ORM\OneToOne(targetEntity="App\Entity\Photo", cascade={"persist"})
     */
    private $realPhoto;

    public function __construct()
    {
        $this->dateTime = new DateTime();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getPlanogram(): ?Planogram
    {
        return $this->planogram;
    }

    public function setPlanogram(Planogram $planogram): self
    {
        $this->planogram = $planogram;

        return $this;
    }

    public function getPhoto(): ?Photo
    {
        return $this->photo;
    }

    public function setPhoto(Photo $photo): self
    {
        $this->photo = $photo;

        return $this;
    }

    public function getDateTime(): ?\DateTimeInterface
    {
        return $this->dateTime;
    }

    public function setDateTime(\DateTimeInterface $dateTime): self
    {
        $this->dateTime = $dateTime;

        return $this;
    }

    public function getData()
    {
        return $this->data;
    }

    public function setData(object $data): self
    {
        $this->data = $data;

        return $this;
    }

    public function getRealPhoto(): ?Photo
    {
        return $this->realPhoto;
    }

    public function setRealPhoto(?Photo $realPhoto): self
    {
        $this->realPhoto = $realPhoto;

        return $this;
    }
}
